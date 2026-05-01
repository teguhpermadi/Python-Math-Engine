import hashlib
from typing import List, Dict, Any
from .arithmetic_service import generate_arithmetic_question
from .geometry_service import generate_geometry_question
from .measurement_service import generate_measurement_question
from .algebra_service import generate_algebra_question
from .statistics_service import generate_statistics_question
from .angle_service import generate_angle_question
from ..schemas.request import ArithmeticRequest, NumberType

def derive_sub_seed(master_seed: int, index: int, domain: str) -> int:
    """Menghasilkan sub-seed unik namun deterministik."""
    seed_str = f"{master_seed}:{index}:{domain}"
    return int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) % (10**9)

async def generate_exam_pack(master_seed: int, requirements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    questions = []
    
    for i, req in enumerate(requirements):
        domain = req.get("domain", "arithmetic")
        level = req.get("level", 1)
        sub_seed = derive_sub_seed(master_seed, i, domain)
        
        # Mapping domain ke service yang sesuai
        if domain == "arithmetic":
            # Convert dict to ArithmeticRequest
            ar_req = ArithmeticRequest(
                seed=sub_seed,
                level=level,
                operation=req.get("operation", "addition"),
                number_type=NumberType(req.get("number_type", "natural")),
                with_story=req.get("with_story", False)
            )
            q = await generate_arithmetic_question(ar_req)
            questions.append({"id": i+1, "domain": domain, "content": q.model_dump()})
            
        elif domain == "geometry":
            q = await generate_geometry_question(
                seed=sub_seed, level=level, 
                shape_type=req.get("shape"), 
                with_story=req.get("with_story", False),
                dimension=req.get("dimension", "3D")
            )
            questions.append({"id": i+1, "domain": domain, "content": q})
            
        elif domain == "measurement":
            q = await generate_measurement_question(sub_seed, level, req.get("with_story", False))
            questions.append({"id": i+1, "domain": domain, "content": q})
            
        elif domain == "algebra":
            q = await generate_algebra_question(sub_seed, level)
            questions.append({"id": i+1, "domain": domain, "content": q})
            
        elif domain == "statistics":
            q = await generate_statistics_question(sub_seed, level)
            questions.append({"id": i+1, "domain": domain, "content": q})

        elif domain == "angles":
            q = await generate_angle_question(sub_seed, level, req.get("type"), req.get("with_story", False))
            questions.append({"id": i+1, "domain": domain, "content": q})

    return {
        "master_seed": master_seed,
        "total_questions": len(questions),
        "questions": questions
    }
