import random
from datetime import datetime
from ..schemas.request import ArithmeticRequest
from ..schemas.response import ArithmeticResponse, MetaInfo, ContextInfo, ArithmeticData
from ..core.seed.manager import SeedManager, SeedContext
from ..core.levels.config import get_level_config
from ..core.number_types.registry import NumberType

# Core generators
from ..core.arithmetic.addition import generate_addition
from ..core.arithmetic.subtraction import generate_subtraction
from ..core.arithmetic.multiplication import generate_multiplication
from ..core.arithmetic.division import generate_division
from ..core.arithmetic.power import generate_power
from ..core.arithmetic.root import generate_root
from ..core.arithmetic.modulo import generate_modulo
from ..core.arithmetic.number_properties import generate_gcd_problem, generate_lcm_problem, generate_factorization_problem
from ..core.arithmetic.comparison import generate_comparison, generate_ordering
from ..core.arithmetic.mixed_operations import generate_mixed_operations

from .blueprint import build_arithmetic_blueprint, build_variables
from .distractor import generate_distractors
from .ai_storyteller import ai_storyteller
from ..exceptions import InvalidLevelError, InvalidNumberTypeForLevelError
from ..core.arithmetic.utils import to_latex

async def generate_arithmetic_question(request: ArithmeticRequest) -> ArithmeticResponse:
    """
    Koordinator utama untuk generate soal aritmatika.
    """
    # 1. Setup Seed & Context
    ctx = SeedContext(
        seed=request.seed,
        operation=request.operation,
        level=request.level,
        number_type=request.number_type.value
    )
    seed_manager = SeedManager(ctx)
    rng = seed_manager.rng
    
    # 2. Get Config
    try:
        level_config = get_level_config(request.level)
    except ValueError as e:
        raise InvalidLevelError(str(e))
    
    # 3. Validate NumberType for Level
    if request.number_type not in level_config.allowed_number_types:
        # Special case for some operations that might be allowed regardless
        # (harus konsisten dengan model_validator di ArithmeticRequest)
        if request.operation not in ["gcd", "lcm", "factorization", "modulo"]:
             raise InvalidNumberTypeForLevelError(
                 f"Tipe {request.number_type} tidak diizinkan di Level {request.level}"
             )
    
    # 3. Call Core Generator
    gen_map = {
        "addition": lambda: generate_addition(rng, level_config, request.number_type, request.operand_count),
        "subtraction": lambda: generate_subtraction(rng, level_config, request.number_type),
        "multiplication": lambda: generate_multiplication(rng, level_config, request.number_type, request.operand_count),
        "division": lambda: generate_division(rng, level_config, request.number_type),
        "power": lambda: generate_power(rng, level_config, request.number_type),
        "root": lambda: generate_root(rng, level_config, request.number_type),
        "modulo": lambda: generate_modulo(rng, level_config, request.number_type),
        "gcd": lambda: generate_gcd_problem(rng, level_config),
        "lcm": lambda: generate_lcm_problem(rng, level_config),
        "factorization": lambda: generate_factorization_problem(rng, level_config),
        "comparison": lambda: generate_comparison(rng, level_config, request.number_type),
        "ordering": lambda: generate_ordering(rng, level_config, request.number_type),
        "mixed": lambda: generate_mixed_operations(
            rng, 
            level_config, 
            request.number_type, 
            operation_count=request.operand_count - 1,
            allowed_operations=request.allowed_operations
        )
    }
    
    if request.operation not in gen_map:
        raise ValueError(f"Operasi '{request.operation}' belum diimplementasikan.")
        
    raw_data = gen_map[request.operation]()
    
    # 4. Build Blueprint & Variables
    blueprint = build_arithmetic_blueprint(raw_data, request.operation)
    variables = build_variables(raw_data)
    
    # 5. Generate Distractors
    correct_answer = raw_data["result"]
    choices = [correct_answer]
    if request.with_distractors:
        distractors = generate_distractors(
            correct_answer, 
            request.operation, 
            request.number_type.value, 
            request.distractor_count, 
            rng
        )
        choices.extend(distractors)
    
    # Shuffle choices deterministically using rng
    rng.shuffle(choices)
    
    # 6. Generate Story (Async)
    story = None
    if request.with_story:
        story = await ai_storyteller.generate_story(
            raw_data["expression"],
            raw_data["result"],
            request.operation,
            request.theme,
            rng
        )

    # 7. Construct Response
    return ArithmeticResponse(
        meta=MetaInfo(
            seed=request.seed,
            level=request.level,
            operation=request.operation,
            number_type=request.number_type.value
        ),
        context=ContextInfo(
            story=story,
            theme=request.theme
        ),
        data=ArithmeticData(
            variables=variables,
            expression=raw_data["expression"],
            expression_latex=raw_data.get("expression_latex") or to_latex(raw_data["expression"]),
            blueprint=blueprint,
            answer_choices=choices,
            answer_choices_latex=[to_latex(c) for c in choices],
            correct_answer=correct_answer,
            correct_answer_latex=to_latex(correct_answer),
            answer_type=raw_data["result_type"]
        )
    )
