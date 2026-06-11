import re

from app.services.skills import HR_SKILLS


def extract_email(text):
    match = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    return match.group(0) if match else None


def extract_phone(text):
    match = re.search(
        r'(\+91)?[6-9]\d{9}',
        text
    )

    return match.group(0) if match else None


def extract_name(text):
    lines = text.split("\n")

    for line in lines[:5]:
        if len(line.strip()) > 3:
            return line.strip()

    return "Unknown"


def extract_experience(text):

    match = re.search(
        r'(\d+)\+?\s*years?',
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(0)

    return "Not Found"


def extract_skills(text):

    text_lower = text.lower()

    skills = []

    for skill in HR_SKILLS:
        if skill.lower() in text_lower:
            skills.append(skill)

    return sorted(list(set(skills)))


def analyze_resume(text):

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "experience": extract_experience(text),
        "skills": extract_skills(text)
    }
