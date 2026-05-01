from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.angle_service import generate_angle_question

router = APIRouter(prefix="/angles", tags=["Lines & Angles"])

class AngleRequest(BaseModel):
    seed: int
    level: int
    type: Optional[str] = None # complementary, supplementary, parallel_lines
    with_story: bool = False

@router.post("/generate")
async def generate_angles(request: AngleRequest):
    try:
        return await generate_angle_question(
            request.seed, 
            request.level, 
            request.type, 
            request.with_story
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
