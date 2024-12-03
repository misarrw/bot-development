from app.database.models import async_session
from app.database.models import Deadline
from sqlalchemy import select
import datetime
from aiogram import Bot

from app.database.requests.requests import get_group

async def get_deadlines(tg_id: int):
    async with async_session() as session:
        number_gr = await get_group(tg_id)
        return await session.scalars(select(Deadline).where(Deadline.number_gr == number_gr))
    

