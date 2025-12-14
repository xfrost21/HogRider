import asyncpg
import logging
from src.core.config import settings

class DatabaseManager:
    def __init__(self):
        self.pool = None
        self.logger = logging.getLogger("bot.database")

    async def connect(self):
        """Tworzy pulę połączeń do PostgreSQL"""
        try:
            self.pool = await asyncpg.create_pool(
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                database=settings.POSTGRES_DB,
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                min_size=1,
                max_size=10 # Skalowalność
            )
            self.logger.info("✅ Połączono z bazą danych PostgreSQL.")
        except Exception as e:
            self.logger.critical(f"❌ KRYTYCZNY BŁĄD BAZY DANYCH: {e}")
            raise e

    async def close(self):
        """Zamyka pulę połączeń"""
        if self.pool:
            await self.pool.close()
            self.logger.info("🔒 Połączenie z bazą danych zamknięte.")

    async def execute(self, query: str, *args):
        """Wykonuje zapytanie INSERT/UPDATE/DELETE"""
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query: str, *args):
        """Pobiera wiele wierszy (SELECT)"""
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        """Pobiera jeden wiersz"""
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)