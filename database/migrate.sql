-- Smart Job Recommendation System - Migration Script
-- Adds missing columns to existing tables without losing data

USE smart_jobs;

-- ============================================
-- 1. ALTER users table - add missing columns
-- ============================================
ALTER TABLE users
  ADD COLUMN IF NOT EXISTS phone VARCHAR(20) DEFAULT NULL AFTER password,
  ADD COLUMN IF NOT EXISTS location VARCHAR(100) DEFAULT NULL AFTER phone,
  ADD COLUMN IF NOT EXISTS bio TEXT DEFAULT NULL AFTER location,
  ADD COLUMN IF NOT EXISTS skills TEXT DEFAULT NULL AFTER bio,
  ADD COLUMN IF NOT EXISTS experience TEXT DEFAULT NULL AFTER skills,
  ADD COLUMN IF NOT EXISTS education TEXT DEFAULT NULL AFTER experience,
  ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP AFTER created_at;

-- ============================================
-- 2. ALTER resumes table - add missing columns
-- ============================================
ALTER TABLE resumes
  ADD COLUMN IF NOT EXISTS original_filename VARCHAR(255) DEFAULT NULL AFTER file_path,
  ADD COLUMN IF NOT EXISTS file_size INT DEFAULT NULL AFTER original_filename,
  ADD COLUMN IF NOT EXISTS extracted_skills TEXT DEFAULT NULL AFTER extracted_text,
  ADD COLUMN IF NOT EXISTS processing_status ENUM('pending','processing','completed','failed') DEFAULT 'completed' AFTER extracted_skills;

-- Mark existing resumes as completed since they already have extracted_text
UPDATE resumes SET processing_status = 'completed' WHERE extracted_text IS NOT NULL AND extracted_text != '';
UPDATE resumes SET processing_status = 'failed' WHERE extracted_text IS NULL OR extracted_text = '';

-- ============================================
-- 3. ALTER jobs table - add missing columns
-- ============================================
ALTER TABLE jobs
  ADD COLUMN IF NOT EXISTS job_type ENUM('Full-time','Part-time','Contract','Internship','Remote') DEFAULT 'Full-time' AFTER location,
  ADD COLUMN IF NOT EXISTS experience_level ENUM('Entry Level','Mid Level','Senior Level','Lead','Manager') DEFAULT 'Entry Level' AFTER job_type,
  ADD COLUMN IF NOT EXISTS category VARCHAR(100) DEFAULT NULL AFTER experience_level,
  ADD COLUMN IF NOT EXISTS responsibilities TEXT DEFAULT NULL AFTER description,
  ADD COLUMN IF NOT EXISTS preferred_skills TEXT DEFAULT NULL AFTER required_skills,
  ADD COLUMN IF NOT EXISTS salary_range VARCHAR(100) DEFAULT NULL AFTER salary_lpa,
  ADD COLUMN IF NOT EXISTS application_url VARCHAR(500) DEFAULT NULL AFTER salary_range,
  ADD COLUMN IF NOT EXISTS posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP AFTER application_url,
  ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE AFTER posted_date;

-- Set posted_date for existing jobs to their created_at
UPDATE jobs SET posted_date = created_at WHERE posted_date IS NULL;

-- ============================================
-- 4. ALTER recommendations table - add matching_skills
-- ============================================
ALTER TABLE recommendations
  ADD COLUMN IF NOT EXISTS matching_skills JSON DEFAULT NULL AFTER match_score;

-- ============================================
-- 5. CREATE saved_jobs table if not exists
-- ============================================
CREATE TABLE IF NOT EXISTS saved_jobs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    UNIQUE KEY unique_save (user_id, job_id)
);

SELECT 'Migration completed successfully!' AS status;
