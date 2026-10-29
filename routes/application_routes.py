from flask import Blueprint, render_template, request, redirect, flash, session
from database.db_config import get_connection
from utils.decorators import login_required

application_bp = Blueprint("applications", __name__)


@application_bp.route("/jobs/<int:job_id>/apply", methods=["POST"])
@login_required
def apply_job(job_id):
    """Submit an in-platform job application with selected resume and optional cover note."""
    user_id = session["user_id"]
    cover_note = request.form.get("cover_note", "").strip()
    resume_id_raw = request.form.get("resume_id", "").strip()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Verify job exists
    cursor.execute("SELECT id, title, company, is_active FROM jobs WHERE id = %s", (job_id,))
    job = cursor.fetchone()
    if not job or not job.get("is_active"):
        flash("The selected job is no longer accepting applications.", "warning")
        cursor.close()
        conn.close()
        return redirect(request.referrer or f"/jobs/{job_id}")

    # 2. Prevent duplicate application
    cursor.execute("SELECT id, status FROM applications WHERE user_id = %s AND job_id = %s", (user_id, job_id))
    existing_app = cursor.fetchone()
    if existing_app:
        flash(f"You have already applied for '{job['title']}' at {job['company']}. Current status: {existing_app['status']}.", "info")
        cursor.close()
        conn.close()
        return redirect(f"/jobs/{job_id}")

    # 3. Resolve resume ID (selected from form or latest active resume)
    resume_id = None
    if resume_id_raw and resume_id_raw.isdigit():
        cursor.execute("SELECT id FROM resumes WHERE id = %s AND user_id = %s", (int(resume_id_raw), user_id))
        r_row = cursor.fetchone()
        if r_row:
            resume_id = r_row["id"]

    if not resume_id:
        cursor.execute("SELECT id FROM resumes WHERE user_id = %s ORDER BY created_at DESC LIMIT 1", (user_id,))
        latest_r = cursor.fetchone()
        if latest_r:
            resume_id = latest_r["id"]

    # 4. Insert application record
    cursor.execute(
        """
        INSERT INTO applications (user_id, job_id, resume_id, cover_note, status)
        VALUES (%s, %s, %s, %s, 'Applied')
        """,
        (user_id, job_id, resume_id, cover_note if cover_note else None)
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash(f"🎉 Your application for '{job['title']}' at {job['company']} was submitted successfully!", "success")
    return redirect("/my-applications")


@application_bp.route("/my-applications", methods=["GET"])
@login_required
def my_applications():
    """List all jobs applied to by the authenticated user with live status tracking."""
    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT 
            a.id AS application_id,
            a.status,
            a.cover_note,
            a.applied_at,
            a.updated_at,
            j.id AS job_id,
            j.title,
            j.company,
            j.location,
            j.job_type,
            j.category,
            j.salary_lpa,
            j.salary_range,
            j.application_url,
            r.original_filename AS resume_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.id
        LEFT JOIN resumes r ON a.resume_id = r.id
        WHERE a.user_id = %s
        ORDER BY a.applied_at DESC
        """,
        (user_id,)
    )
    applications_list = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "my_applications.html",
        applications=applications_list,
        total_count=len(applications_list)
    )


@application_bp.route("/applications/<int:app_id>/withdraw", methods=["POST"])
@login_required
def withdraw_application(app_id):
    """Allow user to withdraw a pending application."""
    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, job_id FROM applications WHERE id = %s AND user_id = %s", (app_id, user_id))
    app_record = cursor.fetchone()
    if not app_record:
        flash("Application record not found.", "danger")
        cursor.close()
        conn.close()
        return redirect("/my-applications")

    cursor.execute("DELETE FROM applications WHERE id = %s", (app_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Your application was withdrawn successfully.", "info")
    return redirect("/my-applications")
