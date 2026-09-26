from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import router


app = FastAPI(
    title="LegalEase API",
    description=(
        "AI-powered legal document generation API"
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():

    return {
        "application": "LegalEase",
        "message": "LegalEase API is running.",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }


app.include_router(router)