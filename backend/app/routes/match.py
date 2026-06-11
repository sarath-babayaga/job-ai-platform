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


@router.get("/match/{resume_id}/{job_id}")
def match_resume_to_job(
    resume_id: int,
    job_id: int,
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

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
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

    result = calculate_match_score(
        resume_text,
        job.description
    )

    return {
        "resume_id": resume_id,
        "job_id": job_id,
        "match_score": result["score"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"]
    }