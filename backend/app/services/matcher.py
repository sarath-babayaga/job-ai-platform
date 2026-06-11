from backend.app.services.skills import HR_SKILLS


def extract_skills(text: str):
    text = text.lower()

    found_skills = []

    for skill in HR_SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


def calculate_match_score(
    resume_text: str,
    job_description: str
):
    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        extract_skills(job_description)
    )

    matched = resume_skills.intersection(job_skills)

    missing = job_skills - resume_skills

    if len(job_skills) == 0:
        score = 0
    else:
        score = round(
            (len(matched) / len(job_skills)) * 100,
            2
        )

    return {
        "score": score,
        "matched_skills": sorted(list(matched)),
        "missing_skills": sorted(list(missing))
    }