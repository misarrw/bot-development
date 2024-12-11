from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url = 'mysql+aiomysql://root:Kk4866336@localhost:3306/bot')

async_session = async_sessionmaker(engine) # подключение к БД

class Base(AsyncAttrs, DeclarativeBase): 
    pass


class Absent(Base):
    __tablename__ = 'absents'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(35))
    group: Mapped[str] = mapped_column(String(6))
    subject: Mapped[str] = mapped_column(String(120))
    cnt_gap: Mapped[int] = mapped_column()


class Deadline(Base):
    __tablename__ = 'deadlines'
    id: Mapped[int] = mapped_column(primary_key=True)
    name_deadline: Mapped[str] = mapped_column(String(120))
    group: Mapped[str] = mapped_column(String(6))
    day: Mapped[str] = mapped_column(String(2))
    month: Mapped[str] = mapped_column(String(2))
    year: Mapped[str] = mapped_column(String(4))
    hour: Mapped[str] = mapped_column(String(2))
    minute: Mapped[str] = mapped_column(String(2))


class Object(Base):
    __tablename__ = 'objects'
    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column(String(120))


class Password(Base):
    __tablename__ = 'passwords'
    id: Mapped[int] = mapped_column(primary_key = True)
    group: Mapped[str] = mapped_column(String(6))
    password: Mapped[str] = mapped_column(String(50))



class Schedule(Base):
    __tablename__ = 'schedules'
    id: Mapped[int] = mapped_column(primary_key=True)
    group: Mapped[str] = mapped_column(String(6))
    monday: Mapped[str] = mapped_column(String(1000))
    tuesday: Mapped[str] = mapped_column(String(1000))
    wednesday: Mapped[str] = mapped_column(String(1000))
    thursday: Mapped[str] = mapped_column(String(1000))
    friday: Mapped[str] = mapped_column(String(1000))
    saturday: Mapped[str] = mapped_column(String(1000))
    '''category: Mapped[int] = mapped_column(ForeignKey('categories.id'))'''


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(35))
    tg_id = mapped_column(BigInteger)
    group: Mapped[int] = mapped_column()
    status: Mapped[bool] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)