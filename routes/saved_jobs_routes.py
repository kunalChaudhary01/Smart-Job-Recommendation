from flask import Blueprint, render_template, request, redirect, flash, session
from database.db_config import get_connection
from utils.decorators import login_required

saved_jobs_bp = Blueprint("saved_jobs", __name__)


@saved_jobs_bp.route("/jobs/save/<int:job_id>", methods=["POST"])
@login_required
def toggle_save_job(job_id):
    """Toggle saving or unsaving a job for the logged-in user."""
    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Verify job exists
    cursor.execute("SELECT id, title, company FROM jobs WHERE id=%s", (job_id,))
    job = cursor.fetchone()

    if not job:
        flash("Job not found", "danger")
        cursor.close()
        conn.close()
        return redirect(request.referrer or "/jobs")

    # Check if already saved
    cursor.execute(
        "SELECT id FROM saved_jobs WHERE user_id=%s AND job_id=%s",
        (user_id, job_id)
    )
    existing_save = cursor.fetchone()

    if existing_save:
        cursor.execute(
            "DELETE FROM saved_jobs WHERE user_id=%s AND job_id=%s",
            (user_id, job_id)
        )
        conn.commit()
        flash(f"Removed '{job['title']}' from saved jobs.", "info")
    else:
        cursor.execute(
            "INSERT INTO saved_jobs (user_id, job_id) VALUES (%s, %s)",
            (user_id, job_id)
        )
        conn.commit()
        flash(f"Saved '{job['title']}' to your saved jobs!", "success")

    cursor.close()
    conn.close()

    return redirect(request.referrer or "/saved-jobs")


@saved_jobs_bp.route("/saved-jobs", methods=["GET"])
@login_required
def saved_jobs():
    """List all saved jobs for the current user."""
    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT 
            j.id, j.title, j.company, j.location, j.job_type,
            j.experience_level, j.category, j.description,
            j.required_skills, j.preferred_skills, j.salary_lpa,
            j.salary_range, j.application_url, j.posted_date,
            sj.saved_at
        FROM saved_jobs sj
        JOIN jobs j ON sj.job_id = j.id
        WHERE sj.user_id = %s
        ORDER BY sj.saved_at DESC
        """,
        (user_id,)
    )
    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("saved_jobs.html", jobs=jobs, total_count=len(jobs))
