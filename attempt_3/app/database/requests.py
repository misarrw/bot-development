from app.database.models import async_session
from app.database.models import User, Password, Schedule, Object, Deadline, Absent
from sqlalchemy import select
import hashlib


async def add_subject(subject: str) -> bool:
    async with async_session() as session:
        if await session.scalar(select(Object).where(Object.subject == subject)):
            return False
        else:
            session.add(Object(subject=subject))
            await session.commit()
            return True


async def check_password(group: str, password: str) -> bool:
    async with async_session() as session:
        hash_password = hashlib.md5(password.encode())
        return await session.scalar(select(Password).where(Password.group == group).
                                    where(Password.password == hash_password.hexdigest()))


async def check_status(tg_id: int) -> bool:
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id).where(User.status))


async def check_student(name: str, group: str) -> bool:
    async with async_session() as session:
        return await session.scalar(select(User).where(User.username == name)
                                       .where(User.group == group))


async def get_absents(tg_id: int) -> list:
    async with async_session() as session:
        group = await get_group(tg_id)
        all_absents = await session.scalars(select(Absent).where(Absent.group == group))
        absents_list = []
        for absent in all_absents:
            absents_list.append(f'{absent.username} {str(absent.cnt_gap)}\n')
        return sorted(absents_list)


async def get_cnt_gap(username: str) -> int:
    async with async_session() as session:
        str_user = await session.scalars(select(Absent).where(Absent.username == username))
        cnt_gap = [i.cnt_gap for i in str_user]
        return cnt_gap[0]


async def get_deadlines(tg_id: int):
    async with async_session() as session:
        group = await get_group(tg_id)
        return await session.scalars(select(Deadline).where(Deadline.group == group))


async def get_group(tg_id: int) -> str:
    async with async_session() as session:
        str_user = await session.scalars(select(User).where(User.tg_id == tg_id))
        group = [i.group for i in str_user]
        return group[0]


async def get_subjects():
    async with async_session() as session:
        return await session.scalars(select(Object))


async def get_schedule(tg_id):
    async with async_session() as session:
        group_schedule = await get_group(tg_id)
        return await session.scalars(
            select(Schedule).where(Schedule.group == group_schedule))


async def get_users(tg_id: int):
    async with async_session() as session:
        group = await get_group(tg_id)
        return await session.scalars(select(User).where(User.group == group))


async def get_user_name(tg_id: int) -> str:
    async with async_session() as session:
        return session.scalars(select(User).where(User.tg_id == tg_id)).username


async def get_user_skips(tg_id: int) -> list:
    async with async_session() as session:
        user_name = await get_user_name(tg_id)
        skips = await session.scalars(select(Absent).where(Absent.username == user_name))
        skips_list = []
        for skip in skips:
            skips_list.append(f'{skip.subject} {str(skip.cnt_gap)}\n')
        return sorted(skips_list)


async def set_absent(username: str, group: str, name_object: str) -> None:
    async with async_session() as session:
        if await session.scalar(select(Absent).where(Absent.subject == name_object).where(Absent.username
                                                                                              == username)):
            str_absent = await session.scalars(select(Absent).where(Absent.subject == name_object)
                                               .where(Absent.username == username))
            for i in str_absent:
                i.cnt_gap += 1
            await session.commit()
        else:
            session.add(Absent(username=username, group=group, name_object=name_object, cnt_gap=1))
            await session.commit()


async def set_deadline(name_deadline: str, group: str, day: str, month: str, year: str, hour: str, minute: str) -> None:
    async with async_session() as session:
        session.add(Deadline(name_deadline=name_deadline, group=group, day=day, month = month, year = year, hour = hour, minute = minute))
        await session.commit()


async def set_user_id(tg_id: int) -> bool:
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def set_user(name: str, tg_id: int, group: str, status: bool) -> None:
    async with async_session() as session:
        session.add(User(username=name, tg_id=tg_id, group=group, status=status))
        await session.commit()
