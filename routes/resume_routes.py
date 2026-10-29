from flask import Blueprint, request, redirect, flash, session, render_template, current_app
from werkzeug.utils import secure_filename
import os
import uuid
from database.db_config import get_connection
from utils.resume_parser import extract_text
from utils.skill_gap import extract_skills
from utils.decorators import login_required

resume_bp = Blueprint("resume", __name__)

ALLOWED_EXTENSIONS = {"pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@resume_bp.route("/upload", methods=["GET"])
@login_required
def upload_page():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, file_path, original_filename, file_size, extracted_skills, processing_status, created_at "
        "FROM resumes WHERE user_id=%s ORDER BY created_at DESC",
        (session["user_id"],)
    )
    resumes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("upload_resume.html", resumes=resumes)


@resume_bp.route("/upload-resume", methods=["POST"])
@login_required
def upload_resume():
    if "resume" not in request.files:
        flash("No file selected", "danger")
        return redirect("/upload")

    file = request.files["resume"]

    if file.filename == "":
        flash("No file selected", "danger")
        return redirect("/upload")

    if not allowed_file(file.filename):
        flash("Only PDF files are allowed", "danger")
        return redirect("/upload")

    # Read file to check size
    file_data = file.read()
    file_size = len(file_data)

    if file_size > MAX_FILE_SIZE:
        flash("File size exceeds 5MB limit", "danger")
        return redirect("/upload")

    if file_size == 0:
        flash("The uploaded file is empty", "danger")
        return redirect("/upload")

    original_filename = secure_filename(file.filename)
    extension = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4()}.{extension}"

    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)

    # Save file to disk
    with open(filepath, "wb") as f:
        f.write(file_data)

    conn = get_connection()
    cursor = conn.cursor()

    # Insert resume record with processing status
    cursor.execute(
        """
        INSERT INTO resumes
        (user_id, file_path, original_filename, file_size, processing_status)
        VALUES (%s, %s, %s, %s, 'processing')
        """,
        (session["user_id"], filepath, original_filename, file_size)
    )
    conn.commit()
    resume_id = cursor.lastrowid

    # Extract text and skills
    try:
        extracted_text = extract_text(filepath)
        if not extracted_text or not extracted_text.strip():
            cursor.execute(
                "UPDATE resumes SET processing_status='failed', extracted_text='' WHERE id=%s",
                (resume_id,)
            )
            conn.commit()
            flash("Could not extract text from the PDF. It may be scanned or image-based.", "warning")
            return redirect("/upload")

        # Extract skills
        skills = extract_skills(extracted_text)
        skills_str = ", ".join(sorted(skills)) if skills else ""

        cursor.execute(
            "UPDATE resumes SET extracted_text=%s, extracted_skills=%s, processing_status='completed' WHERE id=%s",
            (extracted_text, skills_str, resume_id)
        )
        conn.commit()
        flash("Resume uploaded and processed successfully!", "success")

    except Exception:
        cursor.execute(
            "UPDATE resumes SET processing_status='failed' WHERE id=%s",
            (resume_id,)
        )
        conn.commit()
        flash("Error processing resume: please try again", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect("/upload")


@resume_bp.route("/resume/delete/<int:resume_id>", methods=["POST"])
@login_required
def delete_resume(resume_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Verify ownership
    cursor.execute(
        "SELECT id, file_path FROM resumes WHERE id=%s AND user_id=%s",
        (resume_id, session["user_id"])
    )
    resume = cursor.fetchone()

    if not resume:
        flash("Resume not found", "danger")
        cursor.close()
        conn.close()
        return redirect("/upload")

    # Delete file from disk
    try:
        if os.path.exists(resume["file_path"]):
            os.remove(resume["file_path"])
    except OSError:
        pass

    # Delete from database (cascades to recommendations via foreign key)
    cursor.execute("DELETE FROM resumes WHERE id=%s", (resume_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Resume deleted successfully", "success")
    return redirect("/upload")