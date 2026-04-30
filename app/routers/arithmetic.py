from fastapi import APIRouter, HTTPException
from ..schemas.request import ArithmeticRequest
from ..schemas.response import ArithmeticResponse, ErrorResponse
from ..services.arithmetic_service import generate_arithmetic_question

router = APIRouter(
    prefix="/arithmetic",
    tags=["Arithmetic"]
)

@router.post("/generate", response_model=ArithmeticResponse)
async def generate_arithmetic(request: ArithmeticRequest):
    """
    Endpoint untuk generate soal aritmatika.
    """
    try:
        return await generate_arithmetic_question(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log unexpected error
        raise HTTPException(status_code=500, detail="Internal Server Error")
