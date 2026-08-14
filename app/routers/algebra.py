from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.algebra_service import generate_algebra_question

router = APIRouter(prefix="/algebra", tags=["Algebra"])

class AlgebraRequest(BaseModel):
    seed: int
    level: int
    with_distractors: bool = True
    distractor_count: int = 3

@router.post("/generate")
async def generate_algebra(request: AlgebraRequest):
    try:
        return await generate_algebra_question(
            request.seed,
            request.level,
            request.with_distractors,
            request.distractor_count,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
