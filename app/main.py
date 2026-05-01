from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config import settings
from app.routers import arithmetic, geometry, measurement, algebra, statistics, angles
from app.exceptions import MathEngineError

app = FastAPI(
    title=settings.APP_NAME,
    description="Microservice for deterministic math problem generation",
    version="2.0.0",
    debug=settings.DEBUG
)

@app.exception_handler(MathEngineError)
async def math_engine_exception_handler(request: Request, exc: MathEngineError):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "error_code": exc.error_code,
            "message": exc.message
        },
    )

app.include_router(arithmetic.router, prefix="/api/v1")
app.include_router(geometry.router, prefix="/api/v1")
app.include_router(measurement.router, prefix="/api/v1")
app.include_router(algebra.router, prefix="/api/v1")
app.include_router(statistics.router, prefix="/api/v1")
app.include_router(angles.router, prefix="/api/v1")

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
