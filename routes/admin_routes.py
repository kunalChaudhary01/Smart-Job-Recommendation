from flask import Blueprint, render_template, request, redirect, flash
from database.db_config import get_connection
from utils.skill_gap import extract_skills
from utils.decorators import login_required
from utils.job_fetcher import fetch_and_import_jobs

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/jobs", methods=["GET"])
@login_required
def admin_jobs():
    """List all jobs in the admin dashboard and view incoming applications."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
    jobs = cursor.fetchall()

    # Fetch recent candidate applications
    cursor.execute(
        """
        SELECT 
            a.id AS application_id,
            a.status,
            a.cover_note,
            a.applied_at,
            u.name AS candidate_name,
            u.email AS candidate_email,
            u.phone AS candidate_phone,
            j.title AS job_title,
            j.company AS job_company,
            r.original_filename AS resume_name,
            r.file_path AS resume_path
        FROM applications a
        JOIN users u ON a.user_id = u.id
        JOIN jobs j ON a.job_id = j.id
        LEFT JOIN resumes r ON a.resume_id = r.id
        ORDER BY a.applied_at DESC
        LIMIT 50
        """
    )
    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin_jobs.html", jobs=jobs, applications=applications)


@admin_bp.route("/admin/jobs/auto-import", methods=["POST"])
@login_required
def auto_import_jobs():
    """Trigger automated real-time job import from external developer job board feeds."""
    limit_raw = request.form.get("limit", "15").strip()
    try:
        limit = max(1, min(50, int(limit_raw)))
    except ValueError:
        limit = 15

    imported, skipped, error_msg = fetch_and_import_jobs(limit=limit)

    if error_msg:
        flash(f"Auto-import encountered an issue: {error_msg}", "danger")
    elif imported == 0 and skipped > 0:
        flash(f"Auto-import finished: {skipped} jobs were already present in database (no duplicates added).", "info")
    else:
        flash(f"🚀 Successfully imported {imported} new jobs automatically! ({skipped} duplicates skipped)", "success")

    return redirect("/admin/jobs")


@admin_bp.route("/admin/applications/<int:app_id>/status", methods=["POST"])
@login_required
def update_application_status(app_id):
    """Admin endpoint to update candidate application status."""
    new_status = request.form.get("status", "").strip()
    valid_statuses = ["Applied", "Under Review", "Interview", "Accepted", "Rejected"]
    
    if new_status not in valid_statuses:
        flash("Invalid status selected.", "warning")
        return redirect("/admin/jobs")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE applications SET status = %s WHERE id = %s", (new_status, app_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash(f"Application #{app_id} status updated to '{new_status}'.", "success")
    return redirect("/admin/jobs#applications-section")


@admin_bp.route("/admin/jobs/extract-skills", methods=["POST"])
@login_required
def extract_job_skills():
    """Extract skills from a pasted job description for admin preview."""
    description = request.form.get("description", "")
    skills = extract_skills(description)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM jobs ORDER BY id DESC")
    jobs = cursor.fetchall()

    cursor.execute(
        """
        SELECT 
            a.id AS application_id,
            a.status,
            a.cover_note,
            a.applied_at,
            u.name AS candidate_name,
            u.email AS candidate_email,
            j.title AS job_title,
            j.company AS job_company
        FROM applications a
        JOIN users u ON a.user_id = u.id
        JOIN jobs j ON a.job_id = j.id
        ORDER BY a.applied_at DESC
        LIMIT 50
        """
    )
    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin_jobs.html",
        jobs=jobs,
        applications=applications,
        extracted_skills=", ".join(sorted(skills)),
        description=description
    )


@admin_bp.route("/admin/jobs/add", methods=["POST"])
@login_required
def add_job():
    """Add a new job opening manually."""
    title = request.form.get("title", "").strip()
    company = request.form.get("company", "").strip()
    location = request.form.get("location", "").strip()
    job_type = request.form.get("job_type", "Full-time").strip() or "Full-time"
    experience_level = request.form.get("experience_level", "Entry Level").strip() or "Entry Level"
    category = request.form.get("category", "").strip() or None
    description = request.form.get("description", "").strip()
    responsibilities = request.form.get("responsibilities", "").strip() or None
    skills = request.form.get("skills", "").strip() or request.form.get("required_skills", "").strip()
    preferred_skills = request.form.get("preferred_skills", "").strip() or None
    salary_lpa_val = request.form.get("salary_lpa", "").strip()
    salary_lpa = float(salary_lpa_val) if salary_lpa_val else None
    salary_range = request.form.get("salary_range", "").strip() or None

    if not title or not company:
        flash("Title and Company are required fields.", "danger")
        return redirect("/admin/jobs")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO jobs
        (
            title,
            company,
            location,
            job_type,
            experience_level,
            category,
            description,
            responsibilities,
            required_skills,
            preferred_skills,
            salary_lpa,
            salary_range,
            source
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Manual')
        """,
        (
            title,
            company,
            location,
            job_type,
            experience_level,
            category,
            description,
            responsibilities,
            skills,
            preferred_skills,
            salary_lpa,
            salary_range
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash(f"Job '{title}' at {company} created successfully!", "success")
    return redirect("/admin/jobs")


@admin_bp.route("/admin/jobs/delete/<int:job_id>", methods=["GET", "POST"])
@login_required
def delete_job(job_id):
    """Delete a job by ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM jobs WHERE id=%s", (job_id,))
    deleted = cursor.rowcount > 0
    conn.commit()

    cursor.close()
    conn.close()

    if deleted:
        flash("Job deleted successfully.", "success")
    else:
        flash("Job not found or already deleted.", "warning")

    return redirect("/admin/jobs")
