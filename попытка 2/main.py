import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router

bot = Bot(token='7946627017:AAEZpHwYuXV5syytjvclO2OQ_49S7zVRp7c')
dp = Dispatcher() # занимается обработкой сообщений от пользователя


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Black out') # убирает ошибку KeyboardInterrupt в терминале

