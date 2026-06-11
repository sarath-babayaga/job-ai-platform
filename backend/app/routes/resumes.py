from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import shutil

from backend.app.database import get_db
from backend.app.models.resume import Resume
from backend.app.services.resume_parser import parse_docx, parse_pdf

router = APIRouter()

UPLOAD_DIR = "resumes"
Path(UPLOAD_DIR).mkdir(exist_ok=True)


@router.post("/resumes/upload")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume = Resume(
        filename=file.filename,
        filepath=file_path
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


@router.get("/resumes")
def get_resumes(db: Session = Depends(get_db)):
    return db.query(Resume).all()


@router.get("/resumes/{resume_id}/parse")
def parse_resume(
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
        text = parse_docx(filepath)

    elif filepath.endswith(".pdf"):
        text = parse_pdf(filepath)

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    return {
        "resume_id": resume.id,
        "filename": resume.filename,
        "text": text
    }