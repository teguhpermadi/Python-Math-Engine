from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.statistics_service import generate_statistics_question

router = APIRouter(prefix="/statistics", tags=["Statistics"])

class StatisticsRequest(BaseModel):
    seed: int
    level: int
    with_distractors: bool = True
    distractor_count: int = 3

@router.post("/generate")
async def generate_statistics(request: StatisticsRequest):
    try:
        return await generate_statistics_question(
            request.seed,
            request.level,
            request.with_distractors,
            request.distractor_count,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
