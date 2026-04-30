import random
from typing import List

def generate_distractors(
    correct_answer: str,
    operation: str,
    number_type: str,
    count: int = 3,
    rng: random.Random = None
) -> List[str]:
    """
    Menghasilkan pilihan jawaban salah yang masuk akal.
    """
    if rng is None:
        rng = random.Random()

    distractors = set()
    
    try:
        val = float(correct_answer) if '/' not in correct_answer else None
        
        # Rule 1: Off-by-one or Off-by-small-amount
        if val is not None:
            if val.is_integer():
                distractors.add(str(int(val) + 1))
                distractors.add(str(int(val) - 1))
            else:
                distractors.add(str(round(val + 0.1, 2)))
                distractors.add(str(round(val - 0.1, 2)))
        
        # Rule 2: Calculation errors based on operation
        if operation == "multiplication" and val is not None:
            distractors.add(str(int(val) + 10)) # Common carrying error
            
        if '/' in correct_answer:
            # Fraction misconceptions
            num, den = map(int, correct_answer.split('/'))
            distractors.add(f"{num + 1}/{den}")
            distractors.add(f"{num}/{den + 1}")
            distractors.add(f"{num + 1}/{den + 1}")
            
    except:
        pass

    # Fill remaining with random values if needed
    while len(distractors) < count:
        distractors.add(str(rng.randint(1, 100)))

    # Ensure correct answer is not in distractors
    if correct_answer in distractors:
        distractors.remove(correct_answer)
        
    final_list = list(distractors)[:count]
    
    # Shuffle is handled by the caller or at the end
    return final_list
