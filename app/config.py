from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Python Math Engine"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    
    LM_STUDIO_URL: str = "http://localhost:1234/v1"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
