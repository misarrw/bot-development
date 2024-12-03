from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from app.database.requests.deadlines import get_deadlines
from app.middlewares import DeadlinesMiddleware
from app.handlers import send_deadline



dd_router = Router()

scheduler = AsyncIOScheduler(timezone = 'Europe/Moscow')



dd_router.message.outer_middleware(DeadlinesMiddleware(scheduler))


@dd_router.message(F.text == 'Активировать напоминания о дедлайнах')
async def activate_positive(apscheduler: AsyncIOScheduler, message: Message):
    await message.answer('Уведомления о дедлайнах активированы. Теперь тебе будут приходить напоминания о дедлайне в день дедлайна.')
    apscheduler.add_job(send_deadline, 
                        trigger='date', 
                        run_date=datetime.now() + timedelta(seconds=10),
                        kwargs={'message': Message})