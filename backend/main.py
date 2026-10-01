"""
Skill Gap Navigator — FastAPI Backend Entry Point
Run: uvicorn main:app --reload --port 8000
"""

import sys
import os

# Ensure backend directory is on the Python path
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routers.analyze import router as analyze_router

# ── App Setup ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Skill Gap Navigator API",
    description=(
        "AI-powered resume analysis engine that extracts skills, "
        "performs gap analysis against job descriptions, and generates "
        "personalized learning roadmaps."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS (allow all origins for local dev) ────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────

app.include_router(analyze_router)

# ── Health Check ─────────────────────────────────────────────────────────────

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "service": "Skill Gap Navigator API", "version": "1.0.0"}


@app.get("/", tags=["System"])
async def root():
    return {
        "message": "Skill Gap Navigator API",
        "docs": "/docs",
        "health": "/health",
        "analyze": "POST /api/analyze",
    }
