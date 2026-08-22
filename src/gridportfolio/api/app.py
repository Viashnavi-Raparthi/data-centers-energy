"""
FastAPI application.

Run with:

    uvicorn gridportfolio.api.app:app --reload
"""

from fastapi import FastAPI

from gridportfolio.api.routes import router


app = FastAPI(
    title="GridPortfolio",
    description=(
        "Open-source AI-accelerated energy portfolio "
        "integration reference architecture."
    ),
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
def root() -> dict:
    return {
        "name": "GridPortfolio",
        "message": (
            "Energy portfolio connective tissue for "
            "fragmented specialist organizations."
        ),
        "docs": "/docs",
    }