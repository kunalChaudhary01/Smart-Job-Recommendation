"""Database migration script for direct job applications and automated feed integration."""
import sys
import os

sys.path.insert(0, r"d:\Projects\smart-job-recommendation")
from dotenv import load_dotenv

load_dotenv(r"d:\Projects\smart-job-recommendation\.env")
from database.db_config import get_connection


def migrate():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Create applications table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        job_id INT NOT NULL,
        resume_id INT DEFAULT NULL,
        cover_note TEXT DEFAULT NULL,
        status ENUM('Applied', 'Under Review', 'Interview', 'Accepted', 'Rejected') DEFAULT 'Applied',
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
        FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE SET NULL,
        UNIQUE KEY unique_user_job (user_id, job_id)
    )
    """)
    print("Applications table verified/created.")

    # 2. Add source / external_id columns to jobs table
    cursor.execute("DESCRIBE jobs")
    cols = [r[0] for r in cursor.fetchall()]

    if "source" not in cols:
        cursor.execute("ALTER TABLE jobs ADD COLUMN source VARCHAR(50) DEFAULT 'Manual' AFTER is_active")
        print("Added 'source' column to jobs table.")

    if "external_id" not in cols:
        cursor.execute("ALTER TABLE jobs ADD COLUMN external_id VARCHAR(150) DEFAULT NULL AFTER source")
        print("Added 'external_id' column to jobs table.")

    conn.commit()
    cursor.close()
    conn.close()
    print("Migration finished successfully.")


if __name__ == "__main__":
    migrate()
