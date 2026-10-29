import re

try:
    from nltk.corpus import stopwords
    stop_words = set(stopwords.words("english"))
except LookupError:
    # Fallback: if NLTK data is not available, use a minimal set
    stop_words = {
        "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "shall", "can", "need", "dare", "ought",
        "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
        "as", "into", "through", "during", "before", "after", "above",
        "below", "between", "out", "off", "over", "under", "again",
        "further", "then", "once", "here", "there", "when", "where", "why",
        "how", "all", "both", "each", "few", "more", "most", "other",
        "some", "such", "no", "nor", "not", "only", "own", "same", "so",
        "than", "too", "very", "just", "because", "but", "and", "or", "if",
        "while", "about", "up", "it", "its", "i", "me", "my", "we", "our",
        "you", "your", "he", "him", "his", "she", "her", "they", "them",
        "their", "what", "which", "who", "whom", "this", "that", "these",
        "those", "am",
    }


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    words = [word for word in text.split() if word not in stop_words]
    return " ".join(words)
