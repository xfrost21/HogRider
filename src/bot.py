import discord
import coc
import logging
from discord.ext import commands
from src.core.config import settings
from src.database.db import DatabaseManager

class ClashBot(commands.Bot):
    def __init__(self):
        # Konfiguracja Intentów (Uprawnień)
        intents = discord.Intents.default()
        intents.members = True     # Potrzebne do zarządzania rolami
        intents.message_content = True 

        super().__init__(
            command_prefix=self.get_prefix_from_db, # Dynamiczny prefix!
            intents=intents,
            help_command=None # Wyłączamy domyślny help, zrobimy własny ładniejszy
        )

        # Inicjalizacja Modułów
        self.db = DatabaseManager()
        
        # Klient CoC (wersja 4.0)
        self.coc_client = coc.Client()

    async def get_prefix_from_db(self, bot, message):
        """Pobiera prefix z bazy danych, fallback do '!'"""
        # Tu w przyszłości dodamy logikę pobierania per-serwer
        return "!" 

    async def setup_hook(self):
        """Metoda uruchamiana PRZED startem bota (Idealna do DB i Loginów)"""
        print("--- 🔄 Inicjalizacja Systemu ---")
        
        # 1. Połącz z Bazą
        await self.db.connect()

        # 2. Zaloguj do CoC API
        try:
            await self.coc_client.login(
                email=settings.COC_EMAIL, 
                password=settings.COC_PASSWORD
            )
            print("✅ Zalogowano do API Clash of Clans (v4.0)")
        except coc.InvalidCredentials:
            print("❌ BŁĄD: Nieprawidłowe dane do API CoC w pliku .env")
            await self.close()

        # 3. Załaduj Rozszerzenia (Cogs)
        # await self.load_extension("src.cogs.admin") # To odkomentujemy później

    async def on_ready(self):
        print(f"--- 🚀 Bot gotowy: {self.user} (ID: {self.user.id}) ---")
        print(f"--- 🛡️  Wersja Discord.py: {discord.__version__} ---")

    async def close(self):
        """Sprzątanie przy wyłączaniu"""
        await self.coc_client.close()
        await self.db.close()
        await super().close()