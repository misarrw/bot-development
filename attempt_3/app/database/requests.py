from models import async_session
from models import User, Password, Schedule, Subject, Deadline, Absent
from sqlalchemy import select
import hashlib


async def add_subject(subject: str) -> bool:
    """Функция добавления предмета в базу данных

    :param subject: Предмет, который добавляем в базу данных
    :type subject: str
    :return: Возвращает усешность процесса
    :rtype: bool
    """
    async with async_session() as session:
        if await session.scalar(select(Subject).where(Subject.subject == subject)):
            return False
        else:
            session.add(Subject(subject=subject))
            await session.commit()
            return True


async def check_password(group: int, password: str) -> bool:
    """Функция проверки пароля

    :param  group: Номер группы пользователя
    :type group: int
    :param password: Введеный пароль
    :type password: str
    :return: Правильность пароля
    :rtype: bool
    """
    async with async_session() as session:
        hash_password = hashlib.md5(password.encode())
        return await session.scalar(select(Password).where(Password.group == group).
                                    where(Password.password == hash_password.hexdigest()))


async def check_status(tg_id: int) -> bool:
    """Проверка статуса пользователя

    :param tg_id: id пользователя
    :type tg_id: int
    :return: Статус пользователя
    :rtype: bool
    """
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id).where(User.status))


async def check_student(username: str, group: int) -> bool:
    """Проверка наличия студента в группе

    :param username: Имя студента
    :type username: str
    :param group: Группа пользователя
    :type group: int
    :return: Наличие студента в группе
    :rtype: bool
    """
    async with async_session() as session:
        return await session.scalar(select(User).where(User.username == username)
                                       .where(User.group == group))


async def get_absents(tg_id: int) -> list:
    """Получение списка с пропусками студентов определенного предмета

    :param tg_id: id пользователя
    :type tg_id: int
    :return: Список пропусков
    :rtype: list
    """
    async with async_session() as session:
        group = await get_group(tg_id)
        all_absents = await session.scalars(select(Absent).where(Absent.group == group))
        absents_list = []
        for absent in all_absents:
            absents_list.append(f'{absent.username} {str(absent.cnt_gap)}\n')
        return sorted(absents_list)


async def get_cnt_gap(username: str) -> int:
    """Получение пропусков студента

    :param username: Имя студента
    :type username: str
    :return: Пропуски студента
    :rtype: int
    """
    async with async_session() as session:
        str_user = await session.scalars(select(Absent).where(Absent.username == username))
        cnt_gap = [i.cnt_gap for i in str_user]
        return cnt_gap[0]


async def get_deadlines(tg_id: int):
    """Получение списка дедлайнов

    :param tg_id: id пользователя
    :type tg_id: int
    :return: Список дедлайнов
    :rtype:
    """
    async with async_session() as session:
        group = await get_group(tg_id)
        return await session.scalars(select(Deadline).where(Deadline.group == group))


async def get_group(tg_id: int) -> str:
    """Получение группы пользователя

    :param tg_id: id пользователя
    :type tg_id: int
    :return: Группу пользователя
    :rtype: str
    """
    async with async_session() as session:
        str_user = await session.scalars(select(User).where(User.tg_id == tg_id))
        group = [i.group for i in str_user]
        return group[0]


async def get_schedule(tg_id):
    """Получение расписания

    :param tg_id: id пользователя
    :type tg_id: int
    :return: Расписание
    :rtype:
    """
    async with async_session() as session:
        group_schedule = await get_group(tg_id)
        return await session.scalars(
            select(Schedule).where(Schedule.group == group_schedule))



async def get_subjects():
    """Получение списка предметов

    :return: Список предметов
    :rtype:
    """
    async with async_session() as session:
        return await session.scalars(select(Subject))



async def get_users(tg_id: int):
    """Получение списка студентов в группе

    :param tg_id: id пользователя
    :type tg_id: int
    :return: Список студентов
    :rtype:
    """
    async with async_session() as session:
        group = await get_group(tg_id)
        return await session.scalars(select(User).where(User.group == group))


async def get_username(tg_id: int) -> str:
    """Получение имени пользователя

    :param tg_id: id пользователя
    :type tg_id: int
    :return: Имя пользователя
    :rtype: str
    """
    async with async_session() as session:
        return session.scalars(select(User).where(User.tg_id == tg_id)).username


async def get_user_id(tg_id: int) -> bool:
    """Проверка наличия пользователя в базе данных

    :param tg_id: id пользователя
    :type tg_id: int
    :return: Наличие пользователя в базе данных
    :rtype: bool
    """
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_user_skips(tg_id: int) -> list:
    """Получение пропусков пользователя

    :param tg_id: id пользователя
    :type tg_id: int
    :return: Пропуски пользователя
    :rtype: list
    """
    async with async_session() as session:
        user_name = await get_username(tg_id)
        skips = await session.scalars(select(Absent).where(Absent.username == user_name))
        skips_list = []
        for skip in skips:
            skips_list.append(f'{skip.subject} {str(skip.cnt_gap)}\n')
        return sorted(skips_list)


<<<<<<< HEAD
async def set_absent(username: str, group: int, subject: str, number: int) -> None:
    """Заполнение в базе данных информацию о пропусках студентов

    :param username: Имя студента
    :type username: str
    :param group: Группа студента
    :type group: int
    :param subject: Предмет
    :type subject: str
    :param number: Количество пропусков
    :type number: int
    :rtype: None
    """
    async with async_session() as session:
        if await session.scalar(select(Absent).where(Absent.subject == subject).where(Absent.username
                                                                                              == username)):
            str_absent = await session.scalars(select(Absent).where(Absent.subject == subject)
=======
async def set_absent(username: str, group: str, name_object: str, number: int) -> None:
    async with async_session() as session:
        if await session.scalar(select(Absent).where(Absent.subject == name_object).where(Absent.username
                                                                                              == username)) and number == 1:
            str_absent = await session.scalars(select(Absent).where(Absent.subject == name_object)
>>>>>>> 271ae8e6d775ad5452ddeb7da68782746e4cbf2b
                                               .where(Absent.username == username))
            if number == 1:
                for i in str_absent:
                    i.cnt_gap += 1
                await session.commit()
            else:
                for i in str_absent:
                    i.cnt_gap = number
                await session.commit()
        else:
            session.add(Absent(username=username, group=group, subject=subject, cnt_gap=1))
            await session.commit()


async def set_deadline(name_deadline: str, group: int, day: str, month: str, year: str, hour: str, minute: str) -> None:
    """Заполнение в базу данных информацию о дедлайнах группы

    :param name_deadline: Название дедлайна
    :type name_deadline: str
    :param group: Номер группы
    :type group: int
    :param day: День дедлайна
    :type day: str
    :param month: Месяц дедлайна
    :type month: str
    :param year: Год дедлайна
    :type year: str
    :param hour: Час дедлайна
    :type hour: str
    :param minute: Минута дедлайна
    :type minute: str
    :rtype: None
    """
    async with async_session() as session:
        session.add(Deadline(name_deadline=name_deadline, group=group, day=day, month = month, year = year, hour = hour,
                             minute = minute))
        await session.commit()


async def set_user(name: str, tg_id: int, group: int, status: bool) -> None:
    """Заполнение информации о пользователе в базу данных

    :param name: Имя пользователя
    :type name: str
    :param tg_id: id пользователя
    :type tg_id: int
    :param group: Номер группы пользователя
    :type group: int
    :param status: Статус пользователя
    :type status: bool
    :rtype: None
    """
    async with async_session() as session:
        session.add(User(username=name, tg_id=tg_id, group=group, status=status))
        await session.commit()
