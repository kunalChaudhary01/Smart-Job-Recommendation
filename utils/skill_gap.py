import re

# Comprehensive skill catalog (~80+ skills)
SKILLS = {
    # Core Languages
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",
    ".net",
    "go",
    "golang",
    "ruby",
    "php",
    "swift",
    "kotlin",
    "rust",
    "dart",
    "r",

    # Web & Frontend
    "html",
    "css",
    "bootstrap",
    "react",
    "angular",
    "vue",
    "react native",
    "flutter",
    "android",
    "ios",

    # Backend Frameworks
    "flask",
    "django",
    "node",
    "nodejs",
    "express",
    "spring",
    "rails",
    "laravel",

    # Databases & Caching
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "redis",
    "elasticsearch",

    # DevOps, Cloud & Infrastructure
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "git",
    "github",
    "jenkins",
    "terraform",
    "linux",
    "nginx",
    "kafka",

    # Data Science & Machine Learning
    "machine learning",
    "deep learning",
    "nlp",
    "computer vision",
    "tensorflow",
    "scikit-learn",
    "pandas",
    "numpy",
    "matplotlib",
    "spark",
    "hadoop",
    "sas",

    # Analytics & BI
    "excel",
    "power bi",
    "tableau",

    # Architecture & Methodologies
    "rest api",
    "graphql",
    "microservices",
    "agile",
    "scrum",
    "jira",

    # Tools, Design & Specialized
    "figma",
    "photoshop",
    "cybersecurity",
    "blockchain",
    "unity",
    "jupyter",
    "vscode"
}


def normalize_text(text):
    """Normalize text and fix common OCR scanning and spacing artifacts."""
    if not text:
        return ""

    text = text.lower()

    # OCR spacing and punctuation normalization map
    replacements = {
        "ja v a": "java",
        "ja v ascript": "javascript",
        "p andas": "pandas",
        "bo otstrap": "bootstrap",
        "numpy ": "numpy",
        "vs co de": "vscode",
        "jup yter": "jupyter",
        "py thon": "python",
        "doc ker": "docker",
        "kubern etes": "kubernetes",
        "postgre sql": "postgresql",
        "post gre": "postgresql",
        "tensor flow": "tensorflow",
        "scikit - learn": "scikit-learn",
        "sci kit learn": "scikit-learn",
        "scikit_learn": "scikit-learn",
        "re act": "react",
        "ang ular": "angular",
        "node . js": "nodejs",
        "node.js": "nodejs",
        "node js": "nodejs",
        "spring boot": "spring",
        "powerbi": "power bi",
        "reactnative": "react native",
        "deeplearning": "deep learning",
        "machinelearning": "machine learning",
        "restapi": "rest api",
        "restful api": "rest api",
        "restful apis": "rest api",
        "computervision": "computer vision",
        "micro services": "microservices",
        "c plus plus": "c++",
        "c sharp": "c#",
        "dot net": ".net",
        "dotnet": ".net"
    }

    for wrong, correct in replacements.items():
        text = text.replace(wrong, correct)

    # Collapse multiple whitespaces and linebreaks into single space
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_skills(text):
    """
    Extract recognized technical skills from text using boundary-safe matching.
    Supports single-word, multi-word, and special-character skills (e.g. c++, c#, .net).
    """
    if not text:
        return set()

    text = normalize_text(text)
    found_skills = set()

    # Sort skills by length descending so multi-word variants match before single words
    sorted_skills = sorted(SKILLS, key=len, reverse=True)

    for skill in sorted_skills:
        # Build boundary regex pattern suitable for special characters
        escaped_skill = re.escape(skill)

        # Handle special prefixes/suffixes like c++, c#, .net
        # Left boundary: must not be preceded by alphanumeric or symbol attached to identifiers
        # Right boundary: must not be followed by alphanumeric or symbol
        pattern = rf"(?<![a-zA-Z0-9_#+.]){escaped_skill}(?![a-zA-Z0-9_#+])"

        if re.search(pattern, text):
            found_skills.add(skill)

    return found_skills