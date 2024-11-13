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

class schedule(Base):
    __tablename__ = 'schedules'
    id: Mapped[int] = mapped_column(primary_key=True)
    monday: Mapped[str] = mapped_column(String(5000))
    tuesday: Mapped[str] = mapped_column(String(5000))
    wednesday: Mapped[str] = mapped_column(String(5000))
    thursday: Mapped[str] = mapped_column(String(5000))
    friday: Mapped[str] = mapped_column(String(5000))
    saturday: Mapped[str] = mapped_column(String(5000))
    group: Mapped[str] = mapped_column(ForeignKey('users.number_gr'))

    '''category: Mapped[int] = mapped_column(ForeignKey('categories.id'))'''

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)