from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate

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
def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()


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
