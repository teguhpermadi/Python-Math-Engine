from typing import List, Dict, Any
from ..schemas.response import BlueprintStep, VariableInfo
from ..core.arithmetic.utils import to_latex

def build_arithmetic_blueprint(raw_data: Dict[str, Any], operation: str) -> List[BlueprintStep]:
    """
    Mengubah raw_data dari core menjadi blueprint drag-and-drop.
    """
    steps = []
    
    # Simbol pemetaan
    symbols = {
        "addition": "+",
        "subtraction": "-",
        "multiplication": "×",
        "division": "÷",
        "modulo": "mod",
        "power": "^",
        "root": "√"
    }
    
    symbol = symbols.get(operation, "?")
    
    # Jika core sudah menyediakan steps (seperti di mixed_operations)
    if "steps" in raw_data and isinstance(raw_data["steps"], list) and len(raw_data["steps"]) > 0:
        if isinstance(raw_data["steps"][0], dict):
            for i, s in enumerate(raw_data["steps"]):
                steps.append(BlueprintStep(
                    step=i + 1,
                    op=s.get("operation", operation),
                    op_symbol=symbols.get(s.get("operation"), symbol),
                    inputs=s.get("inputs", []),
                    correct_result=s.get("result", ""),
                    result_type=s.get("result_type", "unknown"),
                    hint=s.get("hint")
                ))
            return steps

    # Default single step
    steps.append(BlueprintStep(
        step=1,
        op=operation,
        op_symbol=symbol,
        inputs=["v1", "v2"],
        correct_result=raw_data["result"],
        result_type=raw_data["result_type"],
        hint=None
    ))
    
    return steps

def build_variables(raw_data: Dict[str, Any]) -> List[VariableInfo]:
    """
    Membangun daftar variabel dari operands.
    """
    vars = []
    if "operands" in raw_data:
        for i, val in enumerate(raw_data["operands"]):
            vars.append(VariableInfo(
                id=f"v{i+1}",
                value=val,
                value_latex=to_latex(val),
                type="unknown" # Bisa diperluas
            ))
    elif "base" in raw_data: # Untuk power
        vars.append(VariableInfo(id="v1", value=raw_data["base"], value_latex=to_latex(raw_data["base"]), type="base"))
        vars.append(VariableInfo(id="v2", value=raw_data["exponent"], value_latex=to_latex(raw_data["exponent"]), type="exponent"))
    elif "radicand" in raw_data: # Untuk root
        vars.append(VariableInfo(id="v1", value=raw_data["radicand"], value_latex=to_latex(raw_data["radicand"]), type="radicand"))
        vars.append(VariableInfo(id="v2", value=str(raw_data["root_degree"]), value_latex=to_latex(str(raw_data["root_degree"])), type="degree"))
        
    return vars
