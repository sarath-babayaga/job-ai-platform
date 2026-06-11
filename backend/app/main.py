from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine

from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job

from app.routes.users import router as user_router
from app.routes.resumes import router as resume_router
from app.routes.jobs import router as job_router
from app.routes.match import router as match_router
from app.routes.recommend import router as recommend_router

# Create tables
User.metadata.create_all(bind=engine)
Resume.metadata.create_all(bind=engine)
Job.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job AI Platform",
    version="1.0.0"
)

# CORS for React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Job AI Platform API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# Routers
app.include_router(user_router)
app.include_router(resume_router)
app.include_router(job_router)
app.include_router(match_router)
app.include_router(recommend_router)
