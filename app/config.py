from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Python Math Engine"
    DEBUG: bool = True
    LM_STUDIO_URL: str = "http://localhost:1234/v1"
    LM_TIMEOUT_SECONDS: float = 60.0
    ENABLE_AI_STORY: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
