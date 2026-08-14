from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.geometry_service import generate_geometry_question, get_available_shapes
from app.services.net_service import generate_shape_net, get_net_supported_shapes

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
    with_distractors: bool = True
    distractor_count: int = 3

class NetRequest(BaseModel):
    shape: str
    seed: int
    is_valid: bool = True

@router.get("/shapes")
async def list_shapes():
    """
    Endpoint untuk mendapatkan daftar semua jenis bangun yang bisa dihasilkan.
    """
    return get_available_shapes()

@router.post("/generate")
async def generate_geometry(request: GeometryRequest):
    try:
        return await generate_geometry_question(
            request.seed, 
            request.level, 
            request.shape, 
            request.with_story,
            request.sides,
            request.dimension,
            request.with_distractors,
            request.distractor_count,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/nets/shapes")
async def list_net_shapes():
    """
    Endpoint untuk mendapatkan daftar semua jenis bangun ruang yang jaring-jaringnya didukung.
    """
    return get_net_supported_shapes()

@router.post("/nets/generate")
async def generate_net(request: NetRequest):
    """
    Endpoint untuk menghasilkan jaring-jaring bangun ruang (baik pola yang benar atau pola yang salah).
    """
    try:
        return generate_shape_net(
            request.shape,
            request.seed,
            request.is_valid
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

