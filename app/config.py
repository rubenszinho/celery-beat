
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    
    redis_url: str = "redis://localhost:6379/0"

    
    celery_broker_url: str = ""  
    celery_result_backend: str = ""  

    
    beat_schedule_cron: str = "0 0,12 * * *"  

    class Config:
        env_file = ".env"
        case_sensitive = False

    def get_broker_url(self) -> str:
        return self.celery_broker_url or self.redis_url

    def get_result_backend(self) -> str:
        return self.celery_result_backend or self.redis_url



settings = Settings()
