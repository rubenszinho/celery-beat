
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    redis_url: str = "redis://localhost:6379/0"

    beat_schedule_cron: str = "0 0,12 * * *"  # Default: Run at 00:00 and 12:00 daily

    class Config:
        env_file = ".env"
        case_sensitive = False



settings = Settings()
