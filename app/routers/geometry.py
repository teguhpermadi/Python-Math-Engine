from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.geometry_service import generate_geometry_question

router = APIRouter(
    prefix="/geometry",
    tags=["Geometry"]
)

class GeometryRequest(BaseModel):
    seed: int
    level: int
    shape: Optional[str] = None
    sides: Optional[int] = None # 3, 4, 5, 6, 7, 8
    dimension: str = "3D" # 2D atau 3D
    with_story: bool = False

@router.post("/generate")
async def generate_geometry(request: GeometryRequest):
    try:
        return await generate_geometry_question(
            request.seed, 
            request.level, 
            request.shape, 
            request.with_story,
            request.sides,
            request.dimension
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
