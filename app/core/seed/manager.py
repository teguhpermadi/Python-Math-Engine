import random
import hashlib
from dataclasses import dataclass

@dataclass(frozen=True)
class SeedContext:
    """Konteks lengkap yang membentuk seed unik per soal."""
    seed: int
    operation: str
    level: int
    number_type: str

class SeedManager:
    """
    Wrapper di atas random.Random untuk seed-based generation.
    Setiap instance bersifat independent.
    """

    def __init__(
        self,
        context: SeedContext | int,
        operation: str = "addition",
        level: int = 1,
        number_type: str = "natural",
    ):
        if isinstance(context, int):
            # Backward compatibility: SeedManager(seed_int) masih didukung.
            context = SeedContext(
                seed=context,
                operation=operation,
                level=level,
                number_type=number_type,
            )
        self._context = context
        self._rng = random.Random()
        self._rng.seed(self._make_deterministic_seed(context))

    @property
    def rng(self) -> random.Random:
        """Instance RNG yang sudah di-seed. Gunakan ini untuk semua operasi random."""
        return self._rng

    def get_rng(self) -> random.Random:
        """Alias kompatibilitas untuk kode lama yang memanggil get_rng()."""
        return self._rng

    @staticmethod
    def _make_deterministic_seed(ctx: SeedContext) -> int:
        """
        Menggabungkan semua parameter menjadi satu seed integer yang deterministik.
        Menggunakan hash SHA-256 untuk distribusi yang merata.
        """
        raw = f"{ctx.seed}:{ctx.operation}:{ctx.level}:{ctx.number_type}"
        hash_bytes = hashlib.sha256(raw.encode()).digest()
        # Mengambil 8 byte pertama untuk dijadikan integer
        return int.from_bytes(hash_bytes[:8], byteorder="big")

    def get_context(self) -> SeedContext:
        return self._context
