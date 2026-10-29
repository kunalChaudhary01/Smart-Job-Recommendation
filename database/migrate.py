"""Database migration script - adds missing columns to existing tables."""
import sys
sys.path.insert(0, r"d:\Projects\smart-job-recommendation")

from dotenv import load_dotenv
load_dotenv(r"d:\Projects\smart-job-recommendation\.env")

from database.db_config import get_connection


def get_columns(cursor, table):
    cursor.execute(f"DESCRIBE {table}")
    return {row[0] for row in cursor.fetchall()}


def add_column(cursor, table, column, definition):
    cols = get_columns(cursor, table)
    if column not in cols:
        sql = f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
        cursor.execute(sql)
        print(f"  + Added {table}.{column}")
    else:
        print(f"  = {table}.{column} already exists")


def main():
    conn = get_connection()
    cursor = conn.cursor()

    print("=== Migrating users table ===")
    add_column(cursor, "users", "phone", "VARCHAR(20) DEFAULT NULL AFTER password")
    add_column(cursor, "users", "location", "VARCHAR(100) DEFAULT NULL AFTER phone")
    add_column(cursor, "users", "bio", "TEXT DEFAULT NULL AFTER location")
    add_column(cursor, "users", "skills", "TEXT DEFAULT NULL AFTER bio")
    add_column(cursor, "users", "experience", "TEXT DEFAULT NULL AFTER skills")
    add_column(cursor, "users", "education", "TEXT DEFAULT NULL AFTER experience")
    add_column(cursor, "users", "updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER created_at")
    conn.commit()

    print("\n=== Migrating resumes table ===")
    add_column(cursor, "resumes", "original_filename", "VARCHAR(255) DEFAULT NULL AFTER file_path")
    add_column(cursor, "resumes", "file_size", "INT DEFAULT NULL AFTER original_filename")
    add_column(cursor, "resumes", "extracted_skills", "TEXT DEFAULT NULL AFTER extracted_text")
    add_column(cursor, "resumes", "processing_status", "ENUM('pending','processing','completed','failed') DEFAULT 'completed' AFTER extracted_skills")
    conn.commit()
    # Mark existing resumes
    cursor.execute("UPDATE resumes SET processing_status='completed' WHERE extracted_text IS NOT NULL AND extracted_text != ''")
    cursor.execute("UPDATE resumes SET processing_status='failed' WHERE extracted_text IS NULL OR extracted_text = ''")
    conn.commit()
    print("  Updated processing_status for existing resumes")

    print("\n=== Migrating jobs table ===")
    add_column(cursor, "jobs", "job_type", "ENUM('Full-time','Part-time','Contract','Internship','Remote') DEFAULT 'Full-time' AFTER location")
    add_column(cursor, "jobs", "experience_level", "ENUM('Entry Level','Mid Level','Senior Level','Lead','Manager') DEFAULT 'Entry Level' AFTER job_type")
    add_column(cursor, "jobs", "category", "VARCHAR(100) DEFAULT NULL AFTER experience_level")
    add_column(cursor, "jobs", "responsibilities", "TEXT DEFAULT NULL AFTER description")
    add_column(cursor, "jobs", "preferred_skills", "TEXT DEFAULT NULL AFTER required_skills")
    add_column(cursor, "jobs", "salary_range", "VARCHAR(100) DEFAULT NULL AFTER salary_lpa")
    add_column(cursor, "jobs", "application_url", "VARCHAR(500) DEFAULT NULL AFTER salary_range")
    add_column(cursor, "jobs", "posted_date", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP AFTER application_url")
    add_column(cursor, "jobs", "is_active", "BOOLEAN DEFAULT TRUE AFTER posted_date")
    conn.commit()
    # Set posted_date for existing jobs
    cursor.execute("UPDATE jobs SET posted_date = created_at WHERE posted_date IS NULL")
    conn.commit()
    print("  Updated posted_date for existing jobs")

    print("\n=== Migrating recommendations table ===")
    add_column(cursor, "recommendations", "matching_skills", "JSON DEFAULT NULL AFTER match_score")
    conn.commit()

    print("\n=== Creating saved_jobs table ===")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_jobs (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            job_id INT NOT NULL,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
            UNIQUE KEY unique_save (user_id, job_id)
        )
    """)
    conn.commit()
    print("  saved_jobs table ready")

    # Verify final state
    print("\n=== Final Schema Verification ===")
    for table in ["users", "resumes", "jobs", "recommendations", "saved_jobs"]:
        cols = get_columns(cursor, table)
        print(f"  {table}: {sorted(cols)}")

    cursor.close()
    conn.close()
    print("\n✓ Migration completed successfully!")


if __name__ == "__main__":
    main()
