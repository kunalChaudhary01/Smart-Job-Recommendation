# Smart Job Recommendation System

An AI-powered web application that matches job seekers with relevant job opportunities using TF-IDF vectorization and cosine similarity analysis of resumes.

## Features

- **AI-Powered Job Matching**: Upload your resume and get personalized job recommendations based on skill analysis
- **Resume Parsing**: Automatic text extraction and skill identification from PDF resumes
- **Skill Gap Analysis**: See matching and missing skills for each job
- **Job Browsing**: Search, filter, and sort through available positions
- **Save Jobs**: Bookmark interesting positions for later review
- **Profile Management**: Maintain your professional profile and skills
- **Admin Panel**: Add and manage job listings

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: MySQL
- **ML/NLP**: scikit-learn (TF-IDF), NLTK, Pandas
- **Resume Parsing**: PyPDF2

## Prerequisites

- Python 3.9+
- MySQL 8.0+
- pip (Python package manager)

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd smart-job-recommendation
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_NAME=smart_jobs
```

### 5. Initialize the database
Run the schema in MySQL:
```bash
mysql -u root -p < database/schema.sql
```

### 6. Seed sample jobs (optional)
```bash
python -m database.seed_jobs
```

### 7. Run the application
```bash
python app.py
```

Open http://localhost:5000 in your browser.

## Project Structure

```
smart-job-recommendation/
├── app.py                    # Flask application factory
├── config.py                 # Configuration
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
├── database/
│   ├── db_config.py          # Database connection
│   ├── schema.sql            # Database schema
│   └── seed_jobs.py          # Sample job data
├── routes/
│   ├── main_routes.py        # Landing page
│   ├── auth_routes.py        # Authentication
│   ├── dashboard_routes.py   # Dashboard
│   ├── resume_routes.py      # Resume upload
│   ├── recommendation_routes.py  # Job recommendations
│   ├── job_routes.py         # Job browsing & details
│   ├── saved_jobs_routes.py  # Saved jobs
│   ├── profile_routes.py     # User profile
│   ├── history_routes.py     # Recommendation history
│   └── admin_routes.py       # Admin job management
├── utils/
│   ├── recommender.py        # TF-IDF recommendation engine
│   ├── resume_parser.py      # PDF text extraction
│   ├── skill_gap.py          # Skill extraction & matching
│   ├── text_preprocessor.py  # Text cleaning
│   └── decorators.py         # Auth decorators
├── templates/                # Jinja2 HTML templates
├── static/
│   ├── css/style.css         # Custom styles
│   └── js/main.js            # Client-side JavaScript
└── uploads/                  # Uploaded resumes (gitignored)
```

## How the Recommendation Engine Works

1. User uploads a PDF resume
2. Text is extracted using PyPDF2
3. Skills are identified from the resume text
4. TF-IDF vectors are computed for the resume and all job descriptions
5. Cosine similarity scores determine how well the resume matches each job
6. Top 10 matches are returned with matching/missing skill analysis

> **Note**: Match scores represent text similarity between your resume and job descriptions. They are not a guarantee of job suitability.

## License

This project is for educational purposes.
