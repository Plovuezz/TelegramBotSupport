from aiogram import Bot, Dispatcher
import asyncio

from app.config import get_settings
from app.handlers import messages

settings = get_settings()


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(messages.router)

    print("Success")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
