from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime

class MetaInfo(BaseModel):
    seed: int
    level: int
    operation: str
    number_type: str
    generated_at: datetime = datetime.now()

class ContextInfo(BaseModel):
    story: Optional[str] = None
    theme: str = "general"

class VariableInfo(BaseModel):
    id: str
    label: Optional[str] = None
    value: str
    value_latex: Optional[str] = None
    unit: Optional[str] = None
    type: str

class BlueprintStep(BaseModel):
    step: int
    op: str
    op_symbol: str
    inputs: List[str]
    correct_result: str
    result_type: str
    hint: Optional[str] = None

class ArithmeticData(BaseModel):
    variables: List[VariableInfo]
    expression: str
    expression_latex: Optional[str] = None
    blueprint: List[BlueprintStep]
    answer_choices: List[str]
    answer_choices_latex: Optional[List[str]] = None
    correct_answer: str
    correct_answer_latex: Optional[str] = None
    answer_type: str

class ArithmeticResponse(BaseModel):
    status: str = "success"
    meta: MetaInfo
    context: ContextInfo
    data: ArithmeticData

class ErrorResponse(BaseModel):
    status: str = "error"
    error_code: str
    message: str
    detail: Optional[Dict[str, Any]] = None
