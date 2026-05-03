import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from app.core.arithmetic.utils import to_latex
from app.core.arithmetic.mixed_operations import generate_mixed_operations
from app.core.levels.config import get_level_config
from app.core.number_types.registry import NumberType
import random
import asyncio

def test_latex_conversion():
    test_cases = [
        ("1 + 2", "1 + 2"),
        ("1/2 + 3/4", "\\frac{1}{2} + \\frac{3}{4}"),
        ("2 \u00d7 3", "2 \\times 3"), # \u00d7 is ×
        ("10 \u00f7 2", "\\frac{10}{2}"), # \u00f7 is ÷, SymPy prefers \frac
        ("\u221a16", "\\sqrt{16}"), # \u221a is √
        ("5^2", "5^{2}"),
        ("11 \u00d7 2", "11 \\times 2"),
        ("2 \u00d7 1/2", "2 \\times \\frac{1}{2}"),
    ]
    
    print("Testing LaTeX Conversion Utility:")
    for expression, expected in test_cases:
        try:
            result = to_latex(expression)
            # Remove spaces for comparison
            status = "PASS" if result.replace(" ", "") == expected.replace(" ", "") else "FAIL"
            print(f"Expr: {expression.encode('ascii', 'replace').decode()} | Result: {result} | {status}")
        except Exception as e:
            print(f"Error on {expression}: {e}")

def test_mixed_latex():
    print("\nTesting Mixed Operations LaTeX:")
    rng = random.Random(42)
    level_config = get_level_config(3)
    
    # Force some complex operations
    data = generate_mixed_operations(rng, level_config, NumberType.INTEGER, operation_count=3)
    print(f"Plain Expression: {data['expression']}")
    print(f"LaTeX Expression: {data['expression_latex']}")

def test_full_response_latex():
    print("\nTesting Full Response LaTeX Fields:")
    from app.services.arithmetic_service import generate_arithmetic_question
    from app.schemas.request import ArithmeticRequest

    request = ArithmeticRequest(
        operation="addition",
        level=3,
        number_type=NumberType.FRACTION,
        seed=123,
        operand_count=2
    )
    
    async def run():
        response = await generate_arithmetic_question(request)
        print(f"Expression: {response.data.expression}")
        print(f"Expression LaTeX: {response.data.expression_latex}")
        
        for i, v in enumerate(response.data.variables):
            print(f"Var {v.id}: {v.value} -> LaTeX: {v.value_latex}")
        
        print(f"Correct Answer: {response.data.correct_answer} -> LaTeX: {response.data.correct_answer_latex}")
        print(f"Choices LaTeX: {response.data.answer_choices_latex}")

    asyncio.run(run())

if __name__ == "__main__":
    # Ensure stdout handles UTF-8 for printing symbols like √
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    test_latex_conversion()
    test_mixed_latex()
    test_full_response_latex()
