from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.measurement_service import generate_measurement_question

router = APIRouter(prefix="/measurement", tags=["Measurement"])

class MeasurementRequest(BaseModel):
    seed: int
    level: int
    with_story: bool = False
    with_distractors: bool = True
    distractor_count: int = 3

@router.post("/generate")
async def generate_measurement(request: MeasurementRequest):
    try:
        return await generate_measurement_question(
            request.seed,
            request.level,
            request.with_story,
            request.with_distractors,
            request.distractor_count,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
