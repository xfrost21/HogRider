import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Sekcja Discord
    DISCORD_TOKEN: str
    
    # Sekcja Clash of Clans
    COC_EMAIL: str
    COC_PASSWORD: str
    
    # Sekcja Bazy Danych
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432 # Domyślnie 5432, jeśli nie podano

    class Config:
        env_file = ".env"
        extra = "ignore" # Ignoruj inne zmienne w .env (np. te od pgAdmina)

# Singleton ustawień - używamy tego w całym projekcie
settings = Settings()