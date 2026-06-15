from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.application import Application
from app.models.resume import Resume
from app.models.job import Job

from app.schemas.application import (
    ApplicationCreate
)

from app.services.email_service import (
    send_application_email
)

from app.services.resume_parser import (
    parse_docx,
    parse_pdf
)

from app.services.resume_analyzer import (
    analyze_resume
)

from app.services.matcher import (
    calculate_match_score
)

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post("/")
def apply_job(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):

    new_application = Application(
        resume_id=application.resume_id,
        job_id=application.job_id,
        status="Applied"
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == application.resume_id
        )
        .first()
    )

    job = (
        db.query(Job)
        .filter(
            Job.id == application.job_id
        )
        .first()
    )

    if resume and job:

        filepath = resume.filepath

        if filepath.endswith(".docx"):
            resume_text = parse_docx(filepath)

        elif filepath.endswith(".pdf"):
            resume_text = parse_pdf(filepath)

        else:
            resume_text = ""

        profile = analyze_resume(
            resume_text
        )

        result = calculate_match_score(
            resume_text,
            job.description
        )

        send_application_email(
            candidate_name=profile["name"],
            job_title=job.title,
            company=job.company,
            location=job.location,
            match_score=result["score"]
        )

    return new_application


@router.get("/")
def get_applications(
    db: Session = Depends(get_db)
):
    return db.query(Application).all()