from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db

from backend.app.models.resume import Resume
from backend.app.models.job import Job

from backend.app.services.resume_parser import (
    parse_docx,
    parse_pdf
)

from backend.app.services.matcher import (
    calculate_match_score
)

router = APIRouter()


@router.get("/recommend-jobs/{resume_id}")
def recommend_jobs(
    resume_id: int,
    db: Session = Depends(get_db)
):
    resume = (
        db.query(Resume)
        .filter(Resume.id == resume_id)
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    filepath = resume.filepath

    if filepath.endswith(".docx"):
        resume_text = parse_docx(filepath)

    elif filepath.endswith(".pdf"):
        resume_text = parse_pdf(filepath)

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    jobs = db.query(Job).all()

    recommendations = []

    for job in jobs:

        result = calculate_match_score(
            resume_text,
            job.description
        )

        recommendations.append(
            {
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "match_score": result["score"]
            }
        )

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return recommendations