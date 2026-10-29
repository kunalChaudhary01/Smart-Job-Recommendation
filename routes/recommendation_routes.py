import json
from flask import Blueprint, render_template, session, request
from database.db_config import get_connection
from utils.decorators import login_required
from utils.recommender import recommend_jobs

recommendation_bp = Blueprint("recommendation", __name__)


@recommendation_bp.route("/recommendations")
@login_required
def recommendations():
    """Compute and display smart job recommendations for the user's latest resume."""
    user_id = session["user_id"]

    # Filter parameters
    q = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()
    job_type = request.args.get("job_type", "").strip()
    experience_level = request.args.get("experience_level", "").strip()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch latest resume
    cursor.execute(
        """
        SELECT *
        FROM resumes
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (user_id,)
    )
    resume = cursor.fetchone()

    if not resume or not resume.get("extracted_text"):
        cursor.close()
        conn.close()
        return render_template(
            "recommendations.html",
            recommendations=[],
            saved_job_ids=set(),
            total_count=0,
            has_resume=False,
            q=q,
            category=category,
            job_type=job_type,
            experience_level=experience_level
        )

    # Fetch all active jobs
    cursor.execute("SELECT * FROM jobs WHERE is_active = 1")
    jobs = cursor.fetchall()

    # Generate recommendations using TF-IDF + Cosine Similarity
    results = recommend_jobs(resume["extracted_text"], jobs)

    # Delete previous recommendations for this user & resume to prevent duplication
    cursor.execute(
        """
        DELETE FROM recommendations
        WHERE user_id = %s AND resume_id = %s
        """,
        (user_id, resume["id"])
    )

    # Persist top recommendations with matching and missing skills
    for item in results:
        cursor.execute(
            """
            INSERT INTO recommendations
            (user_id, resume_id, job_id, match_score, matching_skills, missing_skills)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                user_id,
                resume["id"],
                item["job_id"],
                item["score"],
                json.dumps(item.get("matching_skills", [])),
                json.dumps(item.get("missing_skills", []))
            )
        )
    conn.commit()

    # Fetch user's saved job IDs to render bookmark states
    cursor.execute("SELECT job_id FROM saved_jobs WHERE user_id = %s", (user_id,))
    saved_job_ids = {row["job_id"] for row in cursor.fetchall()}

    # Distinct categories for filter options
    cursor.execute("SELECT DISTINCT category FROM jobs WHERE category IS NOT NULL AND category != ''")
    categories = [row["category"] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    # Apply in-memory search and category/type filters to recommendation list
    filtered_results = []
    for item in results:
        if q and (q not in item["title"].lower() and q not in item["company"].lower()):
            continue
        if category and item.get("category") != category:
            continue
        if job_type and item.get("job_type") != job_type:
            continue
        if experience_level and item.get("experience_level") != experience_level:
            continue
        filtered_results.append(item)

    job_types = ["Full-time", "Part-time", "Contract", "Internship", "Remote"]
    experience_levels = ["Entry Level", "Mid Level", "Senior Level", "Lead", "Manager"]

    return render_template(
        "recommendations.html",
        recommendations=filtered_results,
        saved_job_ids=saved_job_ids,
        total_count=len(filtered_results),
        has_resume=True,
        resume=resume,
        q=q,
        category=category,
        job_type=job_type,
        experience_level=experience_level,
        categories=categories,
        job_types=job_types,
        experience_levels=experience_levels
    )