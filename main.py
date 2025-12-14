import asyncio
import logging
from src.bot import ClashBot
from src.core.config import settings

# Konfiguracja logowania (Professional Logging)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

async def main():
    bot = ClashBot()
    
    async with bot:
        await bot.start(settings.DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        # Na Windowsie czasem trzeba zmienić Policy dla asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        # Czyste wyjście przy Ctrl+C
        pass