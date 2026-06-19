from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.job import Job
from app.models.resume import Resume

from app.schemas.job import JobCreate

from app.services.job_fetcher import fetch_all_jobs

from app.services.resume_parser import (
    parse_docx,
    parse_pdf
)

from app.services.matcher import (
    calculate_match_score
)

router = APIRouter()


@router.post("/jobs")
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db)
):
    new_job = Job(
        title=job.title,
        company=job.company,
        location=job.location,
        description=job.description
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


@router.get("/jobs")
def get_jobs(
    db: Session = Depends(get_db)
):
    return db.query(Job).all()


@router.delete("/jobs")
def delete_jobs(
    db: Session = Depends(get_db)
):

    deleted = db.query(Job).delete()

    db.commit()

    return {
        "message": "All jobs deleted",
        "deleted_count": deleted
    }


@router.get("/jobs/fetch")
def fetch_jobs(
    db: Session = Depends(get_db)
):

    jobs = fetch_all_jobs()

    saved = 0

    for job_data in jobs:

        exists = (
            db.query(Job)
            .filter(
                Job.title == job_data["title"],
                Job.company == job_data["company"]
            )
            .first()
        )

        if not exists:

            new_job = Job(
                title=job_data.get("title", ""),
                company=job_data.get("company", ""),
                location=job_data.get("location", ""),
                description=job_data.get("description", "")
            )

            db.add(new_job)

            saved += 1

    db.commit()

    return {
        "total_fetched": len(jobs),
        "new_jobs_saved": saved
    }


@router.get("/jobs/hr")
def get_hr_jobs(
    db: Session = Depends(get_db)
):

    keywords = [
        "recruit",
        "recruiter",
        "recruitment",
        "talent",
        "talent acquisition",
        "human resources",
        "hr",
        "people",
        "people operations",
        "staffing",
        "sourcer",
        "hr operations"
    ]

    jobs = db.query(Job).all()

    filtered = []

    for job in jobs:

        text = (
            f"{job.title} {job.description}"
        ).lower()

        if any(
            keyword in text
            for keyword in keywords
        ):
            filtered.append(job)

    return filtered


@router.get("/jobs/hr/matches/{resume_id}")
def get_hr_job_matches(
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

    keywords = [
        "recruit",
        "recruiter",
        "recruitment",
        "talent",
        "talent acquisition",
        "human resources",
        "hr",
        "people",
        "people operations",
        "staffing",
        "sourcer",
        "hr operations"
    ]

    jobs = db.query(Job).all()

    matches = []

    for job in jobs:

        job_text = (
            f"{job.title} {job.description}"
        ).lower()

        if any(
            keyword in job_text
            for keyword in keywords
        ):

            result = calculate_match_score(
                resume_text,
                job_text
            )

            matches.append({
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "match_score": result["score"]
            })

    matches.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return matches[:20]


@router.get("/jobs/{job_id}")
def get_job(
    job_id: int,
    db: Session = Depends(get_db)
):

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

    return job