import re

FORBIDDEN_PATTERNS = [
    r"\b(add|insert|create|update|delete|remove|drop|truncate|alter)\b",
    r"\b(modify|replace)\s+(movie|theater|showtime|booking|record|row|data)\b",
    r"\b(set|change)\s+(movie|price|rating|status)\b",
    r"\b(book|reserve)\s+(ticket|seat)s?\b",
    r"(;\s*(drop|delete|update|insert|alter))",
    r"\b(sql\s+injection)\b",
]


def is_restricted_request(user_message):
    """Block create/update/delete and booking mutations; allow read-only queries."""
    text = user_message.lower().strip()
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def get_restricted_response():
    return (
        "I can only answer read-only questions about movies, theaters, "
        "showtimes, bookings, and the database. I cannot add, update, delete, "
        "or book tickets."
    )
