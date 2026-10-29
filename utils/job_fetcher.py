"""Automated job scraper and live feed importer service.
Fetches verified tech jobs strictly restricted to:
1. Remote / Worldwide roles (job_type = 'Remote' or candidate_location is Worldwide/Remote)
2. Jobs located in India (Bengaluru, Hyderabad, Pune, Mumbai, Delhi, Chennai, Gurgaon, Noida, etc.)
Any role outside India that is not remote is strictly excluded.
"""
import json
import re
import urllib.request
from database.db_config import get_connection
from utils.skill_gap import extract_skills

# Recognized Indian states, regions, and prominent tech cities
INDIAN_LOCATIONS = [
    "india", "bengaluru", "bangalore", "hyderabad", "pune", "mumbai",
    "chennai", "delhi", "new delhi", "noida", "gurgaon", "gurugram",
    "kolkata", "ahmedabad", "kochi", "cochin", "thiruvananthapuram",
    "trivandrum", "chandigarh", "jaipur", "indore", "karnataka",
    "maharashtra", "tamil nadu", "telangana", "haryana", "uttar pradesh"
]


def is_remote_or_india(location_str, is_remote_flag=False, candidate_location=""):
    """
    Check if a job is either Remote/Worldwide OR physically based in India.
    Returns: (bool is_valid, str normalized_job_type, str normalized_location)
    """
    loc_lower = (location_str or "").lower().strip()
    cand_lower = (candidate_location or "").lower().strip()
    
    # 1. Check if remote
    remote_keywords = ["remote", "work from anywhere", "telecommute", "worldwide", "anywhere", "global"]
    is_remote = (
        is_remote_flag or
        any(k in loc_lower for k in remote_keywords) or
        any(k in cand_lower for k in remote_keywords)
    )

    # 2. Check if India-based
    is_india = (
        any(k in loc_lower for k in INDIAN_LOCATIONS) or
        any(k in cand_lower for k in INDIAN_LOCATIONS)
    )

    if not is_remote and not is_india:
        return False, "Full-time", location_str

    # Format normalized type & location
    if is_remote:
        job_type = "Remote"
        if is_india:
            norm_location = f"{location_str} (Remote)" if "remote" not in loc_lower else location_str
        else:
            norm_location = "Remote / Worldwide" if (not location_str or loc_lower in remote_keywords) else f"Remote ({location_str})"
    else:
        job_type = "Full-time"
        norm_location = location_str

    return True, job_type, norm_location


def strip_html_tags(text):
    """Strip HTML markup and collapse extraneous whitespace."""
    if not text:
        return ""
    clean = re.sub(r"<[^>]+>", " ", text)
    clean = re.sub(r"&nbsp;|&amp;|&quot;|&lt;|&gt;", " ", clean)
    clean = re.sub(r"\s+", " ", clean)
    return clean.strip()


def fetch_from_remotive(limit=15):
    """Fetch remote tech jobs from Remotive API."""
    jobs = []
    feed_url = f"https://remotive.com/api/remote-jobs?category=software-dev&limit={limit * 2}"
    req = urllib.request.Request(feed_url, headers={"User-Agent": "SmartJobRecommendationSystem/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw_jobs = data.get("jobs", [])
            for r in raw_jobs:
                valid, j_type, norm_loc = is_remote_or_india(
                    r.get("candidate_required_location") or "Remote",
                    is_remote_flag=True,
                    candidate_location=r.get("candidate_required_location", "")
                )
                if valid:
                    jobs.append({
                        "external_id": f"remotive-{r.get('id')}",
                        "title": r.get("title", "").strip(),
                        "company": r.get("company_name", "Tech Employer").strip(),
                        "location": norm_loc,
                        "job_type": j_type,
                        "description": r.get("description", ""),
                        "tags": r.get("tags") or [],
                        "url": r.get("url") or "",
                        "source": "Remotive (Remote)",
                        "salary_range": r.get("salary") or "Competitive"
                    })
                    if len(jobs) >= limit:
                        break
    except Exception as e:
        print("Remotive fetch error:", e)
    return jobs


def fetch_from_arbeitnow(limit=15):
    """Fetch jobs from Arbeitnow, filtering strictly for Remote or India."""
    jobs = []
    feed_url = "https://arbeitnow.com/api/job-board-api"
    req = urllib.request.Request(feed_url, headers={"User-Agent": "SmartJobRecommendationSystem/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw_jobs = data.get("data", [])
            for r in raw_jobs:
                is_remote_flag = bool(r.get("remote", False))
                loc = r.get("location") or ""
                valid, j_type, norm_loc = is_remote_or_india(loc, is_remote_flag=is_remote_flag)
                
                if valid:
                    jobs.append({
                        "external_id": r.get("slug") or r.get("url") or f"an-{r.get('id', '')}",
                        "title": r.get("title", "").strip(),
                        "company": r.get("company_name", "Tech Employer").strip(),
                        "location": norm_loc,
                        "job_type": j_type,
                        "description": r.get("description", ""),
                        "tags": r.get("tags") or [],
                        "url": r.get("url") or "",
                        "source": "Arbeitnow (Remote/India)",
                        "salary_range": "Competitive"
                    })
                    if len(jobs) >= limit:
                        break
    except Exception as e:
        print("Arbeitnow fetch error:", e)
    return jobs


def fetch_and_import_jobs(limit=15):
    """
    Fetch external jobs strictly restricted to Remote or India.
    Parses required skills and saves to database without duplicate entries.
    Returns: (imported_count, skipped_count, error_msg)
    """
    imported_count = 0
    skipped_count = 0

    # Retrieve from Remotive first (pure remote) and Arbeitnow (remote/India)
    collected = fetch_from_remotive(limit=limit)
    if len(collected) < limit:
        collected += fetch_from_arbeitnow(limit=limit - len(collected))

    if not collected:
        return 0, 0, "No remote or India-based jobs found in current feeds."

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    for item in collected:
        title = item.get("title", "").strip()
        company = item.get("company", "").strip()
        ext_id = item.get("external_id", "")

        if not title or not company:
            continue

        # Prevent duplicates
        cursor.execute(
            "SELECT id FROM jobs WHERE external_id = %s OR (title = %s AND company = %s)",
            (ext_id, title, company)
        )
        if cursor.fetchone():
            skipped_count += 1
            continue

        raw_desc = item.get("description") or ""
        clean_desc = strip_html_tags(raw_desc)
        tags = item.get("tags") or []
        combined_text = f"{title} {company} {' '.join(tags)} {clean_desc[:1200]}"

        # Skill extraction
        found_skills = extract_skills(combined_text)
        required_skills_str = ", ".join(sorted(found_skills)) if found_skills else ", ".join(tags[:6])

        # Categorization
        t_low = title.lower()
        if any(w in t_low for w in ["data", "analyst", "ai", "scientist", "ml"]):
            category = "Data & AI"
        elif any(w in t_low for w in ["frontend", "ui", "ux", "design", "web", "react"]):
            category = "Frontend & Design"
        elif any(w in t_low for w in ["devops", "cloud", "security", "infra", "sre"]):
            category = "DevOps & Cloud"
        elif any(w in t_low for w in ["manager", "product", "lead"]):
            category = "Product & Management"
        else:
            category = "Software Engineering"

        cursor.execute(
            """
            INSERT INTO jobs (
                title, company, location, job_type, experience_level, category,
                description, responsibilities, required_skills, preferred_skills,
                salary_lpa, salary_range, application_url, source, external_id, is_active
            ) VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s, 1
            )
            """,
            (
                title[:250],
                company[:250],
                item.get("location", "Remote / Worldwide")[:200],
                item.get("job_type", "Remote"),
                "Mid Level",
                category,
                clean_desc[:1500] if clean_desc else "Dynamic role imported from verified remote tech feed.",
                "- Build robust, scalable software and distributed services.\n- Collaborate across engineering and product teams.\n- Ensure automated unit testing, documentation, and code reviews.",
                required_skills_str,
                "git, agile, rest api",
                None,
                item.get("salary_range", "Competitive"),
                item.get("url", ""),
                item.get("source", "Remote API"),
                ext_id[:140]
            )
        )
        imported_count += 1

    conn.commit()
    cursor.close()
    conn.close()

    return imported_count, skipped_count, None
