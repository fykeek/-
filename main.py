import os
import asyncio
from aiogram import Bot, Dispatcher, F
from dotenv import load_dotenv
from app.handlers import router
from app.database.models import astnc_name
async def main():
    await astnc_name()
    load_dotenv()
    bot = Bot(token='7579718432:AAEs_vC6JTqBij5eFmJAQzKL9UFIPeI_2ak') #os.getenv('TOKEN')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run((main()))
    except KeyboardInterrupt:
        print('okay')