from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.text_preprocessor import clean_text
from utils.skill_gap import extract_skills


def recommend_jobs(resume_text, jobs):
    """
    Recommend jobs using TF-IDF vectorization and Cosine Similarity.
    
    NOTE ON MATCH SCORE:
    The computed match_score represents mathematical text/keyword cosine similarity 
    between the resume skills/content and job descriptions. It serves as an automated 
    relevance heuristic and does NOT constitute an employment guarantee or absolute 
    suitability assessment.
    """
    if not resume_text or not resume_text.strip():
        return []
    if not jobs:
        return []

    resume_skills = extract_skills(resume_text)
    processed_resume = " ".join(resume_skills) if resume_skills else clean_text(resume_text)

    # If processed resume text is still empty, fallback to clean text
    if not processed_resume.strip():
        processed_resume = clean_text(resume_text)
    if not processed_resume.strip():
        processed_resume = resume_text.strip().lower()

    corpus = [processed_resume]
    for job in jobs:
        combined = (job.get("required_skills", "") or "") + " " + (job.get("description", "") or "")
        cleaned = clean_text(combined)
        corpus.append(cleaned if cleaned.strip() else combined.strip().lower())

    # Calculate TF-IDF vectors and Cosine Similarity with error handling for empty vocabulary
    try:
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(corpus)
        scores = cosine_similarity(vectors[0:1], vectors[1:])[0]
    except (ValueError, Exception):
        # Fallback if vocabulary is empty or vectorization fails
        scores = [0.0] * len(jobs)

    results = []
    for i, score in enumerate(scores):
        job = jobs[i]
        job_skills = extract_skills(job.get("required_skills", "") or "")
        matching = sorted(list(resume_skills & job_skills))
        missing = sorted(list(job_skills - resume_skills))

        # Text cosine similarity scaled to percentage (0 - 100)
        match_score = round(float(score) * 100, 2)

        results.append({
            "job_id": job["id"],
            "title": job["title"],
            "company": job["company"],
            "location": job.get("location", ""),
            "salary_lpa": job.get("salary_lpa"),
            "salary_range": job.get("salary_range", ""),
            "job_type": job.get("job_type", "Full-time"),
            "experience_level": job.get("experience_level", "Entry Level"),
            "category": job.get("category", ""),
            "required_skills": job.get("required_skills", ""),
            "description": job.get("description", ""),
            "application_url": job.get("application_url", ""),
            "score": match_score,
            "matching_skills": matching,
            "missing_skills": missing
        })

    # Sort descending by match score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:10]