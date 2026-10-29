-- Smart Job Recommendation System Database Schema
CREATE DATABASE IF NOT EXISTS smart_jobs;
USE smart_jobs;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20) DEFAULT NULL,
    location VARCHAR(100) DEFAULT NULL,
    bio TEXT DEFAULT NULL,
    skills TEXT DEFAULT NULL,
    experience TEXT DEFAULT NULL,
    education TEXT DEFAULT NULL,
    expected_salary DECIMAL(10,2) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Resumes Table
CREATE TABLE IF NOT EXISTS resumes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) DEFAULT NULL,
    file_size INT DEFAULT NULL,
    extracted_text LONGTEXT,
    extracted_skills TEXT DEFAULT NULL,
    processing_status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Jobs Table
CREATE TABLE IF NOT EXISTS jobs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    job_type ENUM('Full-time', 'Part-time', 'Contract', 'Internship', 'Remote') DEFAULT 'Full-time',
    experience_level ENUM('Entry Level', 'Mid Level', 'Senior Level', 'Lead', 'Manager') DEFAULT 'Entry Level',
    category VARCHAR(100),
    description TEXT,
    responsibilities TEXT,
    required_skills TEXT,
    preferred_skills TEXT,
    salary_lpa DECIMAL(10,2) DEFAULT NULL,
    salary_range VARCHAR(100),
    application_url VARCHAR(500) DEFAULT NULL,
    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Saved Jobs Table
CREATE TABLE IF NOT EXISTS saved_jobs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    job_id INT NOT NULL,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    UNIQUE KEY unique_save (user_id, job_id)
);

-- 5. Recommendations Table
CREATE TABLE IF NOT EXISTS recommendations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    resume_id INT NOT NULL,
    job_id INT NOT NULL,
    match_score DECIMAL(5,2),
    matching_skills JSON DEFAULT NULL,
    missing_skills JSON DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE
);