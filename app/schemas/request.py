from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional
from ..core.number_types.registry import NumberType

ArithmeticOperation = Literal[
    "addition", "subtraction", "multiplication", "division",
    "power", "root", "modulo", "gcd", "lcm", "mixed",
    "comparison", "ordering", "factorization"
]

class ArithmeticRequest(BaseModel):
    # ── Parameter Wajib ──────────────────────────────────────────────────────
    seed: int = Field(..., description="Seed untuk reproducible generation")
    level: int = Field(..., ge=1, le=7, description="Level kesulitan (1–7)")
    operation: ArithmeticOperation = Field(..., description="Jenis operasi matematika")
    number_type: NumberType = Field(..., description="Tipe bilangan yang digunakan")

    # ── Parameter Opsional ───────────────────────────────────────────────────
    operand_count: int = Field(default=2, ge=2, le=5,
                               description="Jumlah operand (untuk penjumlahan/perkalian)")
    with_story: bool = Field(default=False, description="Generate soal cerita via LM Studio (Not implemented yet)")
    with_distractors: bool = Field(default=True, description="Sertakan pilihan jawaban salah")
    distractor_count: int = Field(default=3, ge=2, le=4)
    theme: str = Field(default="general", description="Tema soal cerita")

    # ── Validasi Lintas Field ─────────────────────────────────────────────────
    @model_validator(mode="after")
    def validate_number_type_for_level(self) -> 'ArithmeticRequest':
        from ..core.levels.config import get_level_config
        try:
            cfg = get_level_config(self.level)
            if self.number_type not in cfg.allowed_number_types:
                # Special case for operations that only support certain types (like GCD/LCM)
                if self.operation in ["gcd", "lcm", "modulo", "factorization"] and self.number_type in [NumberType.NATURAL, NumberType.WHOLE, NumberType.INTEGER]:
                     return self
                
                raise ValueError(
                    f"NumberType '{self.number_type}' tidak tersedia di Level {self.level}. "
                    f"Tersedia: {[t.value for t in cfg.allowed_number_types]}"
                )
        except Exception as e:
            if isinstance(e, ValueError): raise e
            # Log error or handle
            pass
        return self
