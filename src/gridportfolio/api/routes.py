"""
FastAPI routes for the GridPortfolio demonstration.
"""

from __future__ import annotations

from fastapi import APIRouter

from gridportfolio.pipeline import run_demo


router = APIRouter(
    prefix="/api",
    tags=["portfolio"],
)


@router.get("/health")
def health() -> dict:
    """API health check."""

    return {
        "status": "healthy",
        "service": "GridPortfolio",
    }


@router.get("/portfolio")
def portfolio() -> dict:
    """Return integrated portfolio intelligence."""

    return run_demo()


@router.get("/signals")
def signals() -> dict:
    """Return detected cross-team signals."""

    result = run_demo()

    return {
        "signals": result["signals"],
    }


@router.get("/brief")
def executive_brief() -> dict:
    """Return latest executive brief."""

    result = run_demo()

    return result["executive_brief"]