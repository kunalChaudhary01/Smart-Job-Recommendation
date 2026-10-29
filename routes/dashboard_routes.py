from flask import Blueprint, render_template, session
from database.db_config import get_connection
from utils.decorators import login_required
import os

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Total active jobs
    cursor.execute("SELECT COUNT(*) AS cnt FROM jobs WHERE is_active = 1")
    total_jobs = cursor.fetchone()["cnt"]

    # Total resumes for user
    cursor.execute("SELECT COUNT(*) AS cnt FROM resumes WHERE user_id=%s", (user_id,))
    total_resumes = cursor.fetchone()["cnt"]

    # Total recommendations for user
    cursor.execute("SELECT COUNT(*) AS cnt FROM recommendations WHERE user_id=%s", (user_id,))
    total_recommendations = cursor.fetchone()["cnt"]

    # Total saved jobs for user
    cursor.execute("SELECT COUNT(*) AS cnt FROM saved_jobs WHERE user_id=%s", (user_id,))
    total_saved_jobs = cursor.fetchone()["cnt"]

    # Total applied jobs for user
    cursor.execute("SELECT COUNT(*) AS cnt FROM applications WHERE user_id=%s", (user_id,))
    total_applications = cursor.fetchone()["cnt"]

    # Average match score for user
    cursor.execute(
        "SELECT ROUND(AVG(match_score), 1) AS avg_score FROM recommendations WHERE user_id=%s",
        (user_id,)
    )
    row = cursor.fetchone()
    avg_match_score = row["avg_score"] if row and row["avg_score"] else None

    # Latest resume
    cursor.execute(
        """SELECT id, file_path, original_filename, file_size, extracted_skills,
           processing_status, created_at
        FROM resumes WHERE user_id=%s ORDER BY created_at DESC LIMIT 1""",
        (user_id,)
    )
    latest_resume = cursor.fetchone()
    if latest_resume:
        latest_resume["file_name"] = os.path.basename(latest_resume.get("original_filename", "") or latest_resume.get("file_path", ""))

    # Recent top 3 recommendations with job info
    cursor.execute(
        """SELECT r.match_score, r.matching_skills, r.missing_skills,
                  j.id AS job_id, j.title, j.company, j.location, j.job_type
        FROM recommendations r
        JOIN jobs j ON r.job_id = j.id
        WHERE r.user_id=%s
        ORDER BY r.match_score DESC
        LIMIT 3""",
        (user_id,)
    )
    recent_recommendations = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        total_jobs=total_jobs,
        total_resumes=total_resumes,
        total_recommendations=total_recommendations,
        total_saved_jobs=total_saved_jobs,
        total_applications=total_applications,
        avg_match_score=avg_match_score,
        latest_resume=latest_resume,
        recent_recommendations=recent_recommendations
    )
