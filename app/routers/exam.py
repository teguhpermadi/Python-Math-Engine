from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.exam_service import generate_exam_pack

router = APIRouter(prefix="/exam", tags=["Exam"])

class ExamRequest(BaseModel):
    master_seed: int
    requirements: List[Dict[str, Any]]

    model_config = {
        "json_schema_extra": {
            "example": {
                "master_seed": 2024,
                "requirements": [
                    {
                        "domain": "arithmetic",
                        "operation": "addition",
                        "level": 1,
                        "number_type": "natural",
                        "with_story": True
                    },
                    {
                        "domain": "geometry",
                        "shape": "cube",
                        "level": 2,
                        "with_story": False
                    },
                    {
                        "domain": "algebra",
                        "level": 3
                    },
                    {
                        "domain": "measurement",
                        "level": 2,
                        "with_story": True
                    }
                ]
            }
        }
    }

@router.post("/generate")
async def generate_exam(request: ExamRequest):
    """
    Generate sekumpulan soal campuran (Arithmetic, Geometry, etc.) 
    berdasarkan master seed tunggal.
    """
    try:
        return await generate_exam_pack(request.master_seed, request.requirements)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
