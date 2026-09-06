from app.core.seed.manager import SeedManager, SeedContext
from app.core.geometry.angles import (
    generate_complementary_angle, 
    generate_supplementary_angle, 
    generate_parallel_line_angles
)
from app.core.geometry.lines import (
    generate_complementary_drawing, 
    generate_supplementary_drawing
)
from app.services.ai_storyteller import ai_storyteller
from app.services.distractor import generate_distractors

async def generate_angle_question(
    seed: int,
    level: int,
    angle_type: str | None = None,
    with_story: bool = False,
    with_distractors: bool = True,
    distractor_count: int = 3,
):
    ctx = SeedContext(seed=seed, operation="angles", level=level, number_type="natural")
    rng = SeedManager(ctx).rng
    
    types = ["complementary", "supplementary"]
    if level >= 4: types.append("parallel_lines")

    # Validasi eksplisit: tipe tidak dikenal TIDAK boleh diam-diam jatuh ke
    # cabang else (parallel_lines). Klien yang salah nama field harus
    # menerima 400, bukan soal dengan tipe yang salah.
    if angle_type is not None and angle_type not in types:
        raise ValueError(
            f"Tipe sudut '{angle_type}' tidak tersedia di Level {level}. Tersedia: {types}"
        )

    target_type = angle_type or rng.choice(types)
    
    drawing_data = None
    if target_type == "complementary":
        res = generate_complementary_angle(rng)
        drawing_data = generate_complementary_drawing(res["angle_a"])
        expression = f"Jika besar sudut x adalah {res['angle_a']} derajat, tentukan besar sudut penyikunya (y)."
        correct_answer = str(res["angle_b"])
    elif target_type == "supplementary":
        res = generate_supplementary_angle(rng)
        drawing_data = generate_supplementary_drawing(res["angle_a"])
        expression = f"Jika besar sudut x adalah {res['angle_a']} derajat, tentukan besar sudut pelurusnya (y)."
        correct_answer = str(res["angle_b"])
    else: # Parallel lines
        res = generate_parallel_line_angles(rng)
        expression = f"Pada dua garis sejajar yang dipotong garis lain, tentukan besar sudut {res['relationship'].replace('_', ' ')} jika sudut pertama adalah {res['angle_1']} derajat."
        correct_answer = str(res["angle_2"])
        drawing_data = {"type": "parallel_lines_schema", "relationship": res["relationship"]}

    story = None
    if with_story:
        story = await ai_storyteller.generate_story(expression, correct_answer, "angles", "konstruksi", rng)

    # Distractors
    answer_choices = [correct_answer]
    if with_distractors:
        dists = generate_distractors(correct_answer, target_type, "natural", distractor_count, rng, "angles")
        answer_choices.extend(dists)
    rng.shuffle(answer_choices)

    return {
        "status": "success",
        "meta": {"seed": seed, "level": level, "operation": "angles", "type": target_type},
        "context": {"story": story, "theme": "konstruksi"},
        "data": {
            "expression": expression,
            "expression_latex": expression,
            "answer_choices": answer_choices,
            "answer_choices_latex": answer_choices,
            "correct_answer": correct_answer,
            "correct_answer_latex": correct_answer,
            "story": story,
            "drawing_data": drawing_data
        }
    }
