from fastapi import FastAPI
from app.config import settings
from app.routers import arithmetic

app = FastAPI(
    title=settings.APP_NAME,
    description="Microservice for deterministic math problem generation",
    version="2.0.0",
    debug=settings.DEBUG
)

app.include_router(arithmetic.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Python Math Engine is running",
        "version": "2.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}
