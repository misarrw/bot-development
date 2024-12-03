from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url = 'mysql+aiomysql://root:Kk4866336@localhost:3306/bot')

async_session = async_sessionmaker(engine) # подключение к БД

class Base(AsyncAttrs, DeclarativeBase): 
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String(35))
    tg_id = mapped_column(BigInteger)
    number_gr: Mapped[str] = mapped_column(String(10))
    status: Mapped[bool] = mapped_column()

class Password(Base):
    __tablename__ = 'passwords'
    id: Mapped[int] = mapped_column(primary_key = True)
    number_gr: Mapped[str] = mapped_column(String(6))
    password: Mapped[str] = mapped_column(String(50))

class Schedule(Base):
    __tablename__ = 'schedules'
    id: Mapped[int] = mapped_column(primary_key=True)
    group: Mapped[str] = mapped_column(String(10))
    monday: Mapped[str] = mapped_column(String(1000))
    tuesday: Mapped[str] = mapped_column(String(1000))
    wednesday: Mapped[str] = mapped_column(String(1000))
    thursday: Mapped[str] = mapped_column(String(1000))
    friday: Mapped[str] = mapped_column(String(1000))
    saturday: Mapped[str] = mapped_column(String(1000))

class Absent(Base):
    __tablename__ = 'absents'
    id: Mapped[int] = mapped_column(primary_key=True)
    name_user: Mapped[str] = mapped_column(String(35))
    number_gr: Mapped[str] = mapped_column(String(6))
    name_object: Mapped[str] = mapped_column(String(120))
    cnt_gap: Mapped[int] = mapped_column()

class Object(Base):
    __tablename__ = 'objects'
    id: Mapped[int] = mapped_column(primary_key=True)
    name_object: Mapped[str] = mapped_column(String(120))


class Deadline(Base):
    __tablename__ = 'deadlines'
    id: Mapped[int] = mapped_column(primary_key=True)
    name_deadline: Mapped[str] = mapped_column(String(120))
    number_gr: Mapped[str] = mapped_column(String(6))
    day: Mapped[str] = mapped_column(String(2))
    month: Mapped[str] = mapped_column(String(2))
    year: Mapped[str] = mapped_column(String(4))
    hour: Mapped[str] = mapped_column(String(2))
    minute: Mapped[str] = mapped_column(String(2))


    '''category: Mapped[int] = mapped_column(ForeignKey('categories.id'))'''

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)