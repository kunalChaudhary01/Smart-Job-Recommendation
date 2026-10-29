import json
from flask import Blueprint, render_template, session
from database.db_config import get_connection
from utils.decorators import login_required

history_bp = Blueprint("history", __name__)


@history_bp.route("/history")
@login_required
def history():
    """View recommendation history for the authenticated user."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            j.id AS job_id,
            j.title,
            j.company,
            j.location,
            j.salary_range,
            j.job_type,
            j.application_url,
            r.match_score,
            r.matching_skills,
            r.missing_skills,
            r.created_at
        FROM recommendations r
        JOIN jobs j ON r.job_id = j.id
        WHERE r.user_id = %s
        ORDER BY r.created_at DESC
        """,
        (session["user_id"],)
    )
    history_data = cursor.fetchall()

    for item in history_data:
        # Safely parse JSON strings for skills lists
        if isinstance(item.get("missing_skills"), str):
            try:
                item["missing_skills"] = json.loads(item["missing_skills"])
            except (json.JSONDecodeError, TypeError):
                item["missing_skills"] = []
        elif item.get("missing_skills") is None:
            item["missing_skills"] = []

        if isinstance(item.get("matching_skills"), str):
            try:
                item["matching_skills"] = json.loads(item["matching_skills"])
            except (json.JSONDecodeError, TypeError):
                item["matching_skills"] = []
        elif item.get("matching_skills") is None:
            item["matching_skills"] = []

    cursor.close()
    conn.close()

    return render_template(
        "history.html",
        history=history_data,
        total_count=len(history_data)
    )