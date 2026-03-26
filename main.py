from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints.minerals import router as minerals_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="REST API for the Democratic Republic of Congo minerals production dataset. 270 records spanning 25 mineral types across 18 provinces (2010–2024).",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(
    minerals_router,
    prefix=f"{settings.API_V1_PREFIX}/minerals",
    tags=["minerals"],
)


@app.get("/", tags=["health"])
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}