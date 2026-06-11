from fastapi import FastAPI

from backend.app.database import engine
from backend.app.models.user import User
from backend.app.routes.users import router as user_router

User.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job AI Platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Job AI Platform API Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

app.include_router(user_router)