from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@profile_db:5432/profile_db"
    KAFKA_BROKERS: str = "kafka:9092"
    KAFKA_TOPIC: str = "user.registered" # Топик который  будем слушать
    KAFKA_GROUP_ID: str = "profile-service-group"

    class Config:
            env_file = ".env" 

settings = Settings()