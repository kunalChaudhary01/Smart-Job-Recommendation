from flask import Blueprint, render_template, request, redirect, flash, session
from database.db_config import get_connection
from utils.decorators import login_required

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET"])
@login_required
def view_profile():
    """View user profile details, skills, and latest resume."""
    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM resumes WHERE user_id=%s ORDER BY created_at DESC LIMIT 1",
        (user_id,)
    )
    latest_resume = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        flash("User not found", "danger")
        return redirect("/login")

    # Parse comma-separated skills into clean list
    skills_list = []
    if user.get("skills"):
        skills_list = [s.strip() for s in user["skills"].split(",") if s.strip()]

    resume_skills_list = []
    if latest_resume and latest_resume.get("extracted_skills"):
        resume_skills_list = [s.strip() for s in latest_resume["extracted_skills"].split(",") if s.strip()]

    return render_template(
        "profile.html",
        user=user,
        skills=skills_list,
        resume_skills=resume_skills_list,
        latest_resume=latest_resume
    )


@profile_bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    """View and update profile information."""
    user_id = session["user_id"]
    conn = get_connection()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip() or None
        location = request.form.get("location", "").strip() or None
        bio = request.form.get("bio", "").strip() or None
        skills = request.form.get("skills", "").strip() or None
        experience = request.form.get("experience", "").strip() or None
        education = request.form.get("education", "").strip() or None
        expected_salary_raw = request.form.get("expected_salary", "").strip()
        expected_salary = float(expected_salary_raw) if expected_salary_raw else None

        if not name:
            flash("Name cannot be empty", "danger")
            conn.close()
            return redirect("/profile/edit")

        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users SET
                name=%s,
                phone=%s,
                location=%s,
                bio=%s,
                skills=%s,
                experience=%s,
                education=%s,
                expected_salary=%s
            WHERE id=%s
            """,
            (name, phone, location, bio, skills, experience, education, expected_salary, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        session["user_name"] = name
        flash("Profile updated successfully!", "success")
        return redirect("/profile")

    # GET request: fetch current user data
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        flash("User not found", "danger")
        return redirect("/login")

    return render_template("profile_edit.html", user=user)


@profile_bp.route("/profile/skills/add", methods=["POST"])
@login_required
def add_skill():
    """Add a skill to the user's skill set."""
    new_skill = request.form.get("skill", "").strip().lower()

    if not new_skill:
        flash("Please provide a valid skill name", "warning")
        return redirect(request.referrer or "/profile")

    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT skills FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    current_skills = []
    if user and user.get("skills"):
        current_skills = [s.strip().lower() for s in user["skills"].split(",") if s.strip()]

    if new_skill not in current_skills:
        current_skills.append(new_skill)
        updated_skills_str = ", ".join(current_skills)

        cursor.execute(
            "UPDATE users SET skills=%s WHERE id=%s",
            (updated_skills_str, user_id)
        )
        conn.commit()
        flash(f"Skill '{new_skill}' added successfully!", "success")
    else:
        flash(f"Skill '{new_skill}' is already in your profile", "info")

    cursor.close()
    conn.close()

    return redirect(request.referrer or "/profile")


@profile_bp.route("/profile/skills/remove", methods=["POST"])
@login_required
def remove_skill():
    """Remove a skill from the user's skill set."""
    skill_to_remove = request.form.get("skill", "").strip().lower()

    if not skill_to_remove:
        flash("Skill to remove not specified", "warning")
        return redirect(request.referrer or "/profile")

    user_id = session["user_id"]
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT skills FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if user and user.get("skills"):
        current_skills = [s.strip() for s in user["skills"].split(",") if s.strip()]
        updated_skills = [s for s in current_skills if s.lower() != skill_to_remove]
        updated_skills_str = ", ".join(updated_skills) if updated_skills else None

        cursor.execute(
            "UPDATE users SET skills=%s WHERE id=%s",
            (updated_skills_str, user_id)
        )
        conn.commit()
        flash(f"Skill '{skill_to_remove}' removed successfully!", "success")

    cursor.close()
    conn.close()

    return redirect(request.referrer or "/profile")
