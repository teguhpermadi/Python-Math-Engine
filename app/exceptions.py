class MathEngineError(Exception):
    """Base exception for all Math Engine errors."""
    def __init__(self, message: str, error_code: str = "INTERNAL_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

# ── Level & Config ───────────────────────────────────────────────────────────
class InvalidLevelError(MathEngineError):
    def __init__(self, message: str):
        super().__init__(message, "INVALID_LEVEL")

class InvalidNumberTypeForLevelError(MathEngineError):
    def __init__(self, message: str):
        super().__init__(message, "INVALID_NUMBER_TYPE_FOR_LEVEL")

class InvalidOperationForLevelError(MathEngineError):
    def __init__(self, message: str):
        super().__init__(message, "INVALID_OPERATION_FOR_LEVEL")

# ── Generation ───────────────────────────────────────────────────────────────
class GenerationFailedError(MathEngineError):
    def __init__(self, message: str):
        super().__init__(message, "GENERATION_FAILED")

class DivisionByZeroError(MathEngineError):
    def __init__(self, message: str):
        super().__init__(message, "DIVISION_BY_ZERO")

class NegativeRadicandError(MathEngineError):
    def __init__(self, message: str):
        super().__init__(message, "NEGATIVE_RADICAND")

# ── External ─────────────────────────────────────────────────────────────────
class LMStudioConnectionError(MathEngineError):
    def __init__(self, message: str):
        super().__init__(message, "LM_STUDIO_CONNECTION_ERROR")
