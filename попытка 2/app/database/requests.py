from app.database.models import async_session
from app.database.models import User, Password
from sqlalchemy import select

async def set_user_id(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            return False
        else:
            return True
        
async def set_user(name: str, tg_id: int, group: str, status: bool):
    async with async_session() as session:
        session.add(User(name_user=name,tg_id=tg_id,number_gr=group,status=status))
        await session.commit()

async def check_password(group: str, password: str):
    async with async_session() as session:
        user = await session.scalar(select(Password).where(Password.number_gr==group).where(Password.password==password))
        if user:
            return True
        else:
            return False