import math
from flask import Blueprint, render_template, request, redirect, flash, session
from database.db_config import get_connection
from utils.decorators import login_required
from utils.skill_gap import extract_skills
from utils.recommender import recommend_jobs

job_bp = Blueprint("jobs", __name__)


@job_bp.route("/jobs", methods=["GET"])
@login_required
def browse_jobs():
    """Browse jobs with multi-facet search, filtering, sorting, and pagination."""
    user_id = session["user_id"]

    # Filter and search params
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    job_type = request.args.get("job_type", "").strip()
    experience_level = request.args.get("experience_level", "").strip()
    location = request.args.get("location", "").strip()
    sort_by = request.args.get("sort_by", "date_desc").strip()

    # Pagination params
    try:
        page = max(1, int(request.args.get("page", 1)))
    except (ValueError, TypeError):
        page = 1
    per_page = 10
    offset = (page - 1) * per_page

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Dynamic WHERE conditions
    where_clauses = ["is_active = 1"]
    params = []

    if q:
        where_clauses.append("(title LIKE %s OR company LIKE %s OR required_skills LIKE %s OR description LIKE %s)")
        wildcard_q = f"%{q}%"
        params.extend([wildcard_q, wildcard_q, wildcard_q, wildcard_q])

    if category:
        where_clauses.append("category = %s")
        params.append(category)

    if job_type:
        where_clauses.append("job_type = %s")
        params.append(job_type)

    if experience_level:
        where_clauses.append("experience_level = %s")
        params.append(experience_level)

    if location:
        where_clauses.append("location LIKE %s")
        params.append(f"%{location}%")

    where_sql = " AND ".join(where_clauses)

    # Sorting
    sort_options = {
        "date_desc": "posted_date DESC, id DESC",
        "date_asc": "posted_date ASC, id ASC",
        "title_asc": "title ASC",
        "title_desc": "title DESC",
        "salary_desc": "salary_lpa DESC, id DESC",
        "salary_asc": "salary_lpa ASC, id ASC"
    }
    order_by_sql = sort_options.get(sort_by, "posted_date DESC, id DESC")

    # Count total matching jobs
    count_sql = f"SELECT COUNT(*) AS total FROM jobs WHERE {where_sql}"
    cursor.execute(count_sql, tuple(params))
    total_count = cursor.fetchone()["total"]
    total_pages = max(1, math.ceil(total_count / per_page))

    # Fetch paginated jobs
    fetch_sql = f"""
        SELECT id, title, company, location, job_type, experience_level,
               category, description, required_skills, preferred_skills,
               salary_lpa, salary_range, application_url, source, posted_date
        FROM jobs
        WHERE {where_sql}
        ORDER BY {order_by_sql}
        LIMIT %s OFFSET %s
    """
    cursor.execute(fetch_sql, tuple(params + [per_page, offset]))
    jobs = cursor.fetchall()

    # Get set of saved job IDs for this user
    cursor.execute("SELECT job_id FROM saved_jobs WHERE user_id=%s", (user_id,))
    saved_job_ids = {row["job_id"] for row in cursor.fetchall()}

    # Get set of applied job IDs for this user
    cursor.execute("SELECT job_id FROM applications WHERE user_id=%s", (user_id,))
    applied_job_ids = {row["job_id"] for row in cursor.fetchall()}

    # Populate filter choices for UI dropdowns
    cursor.execute("SELECT DISTINCT category FROM jobs WHERE category IS NOT NULL AND category != '' ORDER BY category")
    categories = [row["category"] for row in cursor.fetchall()]

    job_types = ["Full-time", "Part-time", "Contract", "Internship", "Remote"]
    experience_levels = ["Entry Level", "Mid Level", "Senior Level", "Lead", "Manager"]

    cursor.close()
    conn.close()

    return render_template(
        "jobs.html",
        jobs=jobs,
        saved_job_ids=saved_job_ids,
        applied_job_ids=applied_job_ids,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        total_count=total_count,
        q=q,
        category=category,
        job_type=job_type,
        experience_level=experience_level,
        location=location,
        sort_by=sort_by,
        categories=categories,
        job_types=job_types,
        experience_levels=experience_levels
    )


@job_bp.route("/jobs/<int:job_id>", methods=["GET"])
@login_required
def job_detail(job_id):
    """View detailed information for a single job with personalized skill analysis and application modal."""
    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM jobs WHERE id=%s", (job_id,))
    job = cursor.fetchone()

    if not job:
        flash("Job not found", "danger")
        cursor.close()
        conn.close()
        return redirect("/jobs")

    # Check if saved by current user
    cursor.execute(
        "SELECT id FROM saved_jobs WHERE user_id=%s AND job_id=%s",
        (user_id, job_id)
    )
    is_saved = cursor.fetchone() is not None

    # Check if already applied by current user
    cursor.execute(
        "SELECT id, status, applied_at FROM applications WHERE user_id=%s AND job_id=%s",
        (user_id, job_id)
    )
    user_application = cursor.fetchone()

    # Fetch user's uploaded resumes
    cursor.execute(
        "SELECT id, original_filename, file_path, created_at FROM resumes WHERE user_id=%s ORDER BY created_at DESC",
        (user_id,)
    )
    user_resumes = cursor.fetchall()

    cursor.close()
    conn.close()

    # Skill matching calculation against latest resume
    match_score = None
    matching_skills = []
    missing_skills = []
    has_resume = False

    latest_resume = user_resumes[0] if user_resumes else None

    if latest_resume:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT extracted_text FROM resumes WHERE id=%s", (latest_resume["id"],))
        r_text_row = cursor.fetchone()
        cursor.close()
        conn.close()

        if r_text_row and r_text_row.get("extracted_text"):
            has_resume = True
            resume_skills = extract_skills(r_text_row["extracted_text"])
            job_skills = extract_skills(job.get("required_skills", "") or "")

            matching_skills = sorted(list(resume_skills & job_skills))
            missing_skills = sorted(list(job_skills - resume_skills))

            single_job_rec = recommend_jobs(r_text_row["extracted_text"], [job])
            if single_job_rec:
                match_score = single_job_rec[0]["score"]
            else:
                match_score = 0.0

    return render_template(
        "job_detail.html",
        job=job,
        is_saved=is_saved,
        user_application=user_application,
        user_resumes=user_resumes,
        has_resume=has_resume,
        match_score=match_score,
        matching_skills=matching_skills,
        missing_skills=missing_skills
    )


@job_bp.route("/jobs/<int:job_id>/redirect", methods=["GET"])
def redirect_to_original_job(job_id):
    """Direct redirection route to the original employer posting URL."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, application_url FROM jobs WHERE id = %s", (job_id,))
    job = cursor.fetchone()
    cursor.close()
    conn.close()

    if not job or not job.get("application_url") or not job["application_url"].strip():
        flash("Original link is not available for this job posting.", "warning")
        return redirect(f"/jobs/{job_id}")

    target_url = job["application_url"].strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        target_url = "https://" + target_url

    return redirect(target_url, code=302)
