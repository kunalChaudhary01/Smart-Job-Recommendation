# Smart Job Recommendation System

An AI-powered web application that matches job seekers with relevant job opportunities using TF-IDF vectorization and cosine similarity analysis of resumes.

## Features

- **AI-Powered Job Matching:** Upload your resume and get personalized job recommendations based on skill analysis.
- **Resume Parsing:** Automatic text extraction and skill identification from PDF resumes.
- **Skill Gap Analysis:** See matching and missing skills for each job.
- **Job Browsing:** Search, filter, and sort available positions.
- **Save Jobs:** Bookmark interesting positions for later review.
- **Profile Management:** Maintain your professional profile and skills.
- **Admin Panel:** Add and manage job listings.

## Technology Stack

- **Backend:** Python, Flask
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Database:** MySQL
- **Machine Learning/NLP:** scikit-learn (TF-IDF), NLTK, Pandas
- **Resume Parsing:** PyPDF2

## Prerequisites

- Python 3.9+
- MySQL 8.0+
- pip (Python package manager)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/kunalChaudhary01/Smart-Job-Recommendation.git
cd Smart-Job-Recommendation
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

On Windows:

```powershell
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_NAME=smart_jobs
```

Replace the example values with your actual configuration. Never commit real passwords, API keys, or secrets to GitHub.

### 5. Initialize the Database

If your project includes `database/schema.sql`, run:

```bash
mysql -u root -p < database/schema.sql
```

### 6. Seed Sample Jobs (Optional)

If your project includes the seed script, run:

```bash
python -m database.seed_jobs
```

### 7. Run the Application

```bash
python app.py
```

Open `http://localhost:5000` in your browser.

## Project Structure

```text
smart-job-recommendation/
├── app.py
├── config.py
├── requirements.txt
├── database/
│   ├── db_config.py
│   ├── schema.sql
│   └── seed_jobs.py
├── routes/
├── utils/
├── templates/
├── static/
└── uploads/
```

The directory structure above is illustrative. Your actual project may contain additional files and folders.

## How the Recommendation Engine Works

1. The user uploads a PDF resume.
2. Text is extracted using PyPDF2.
3. Skills are identified from the resume text.
4. TF-IDF vectors are computed for the resume and job descriptions.
5. Cosine similarity scores determine how well the resume matches each job.
6. The top 10 matches are returned with matching and missing skill analysis.

**Note:** Match scores represent text similarity between a resume and job descriptions. They do not guarantee job suitability.

## License

This project is for educational purposes.