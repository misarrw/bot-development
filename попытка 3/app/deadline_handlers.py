### Импорты
from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


### Импорты из файлов
import app.database.requests.requests as rq
import app.keyboards as kb
from app.middlewares import DDMiddleware
from app.meow import send_deadline
from app.sup_func import check_data



class Deadline(StatesGroup):
    name_deadline = State()
    day_deadline = State()
    time_deadline = State()
    day = State()


deadline_router = Router()


'''deadline_router.message.outer_middleware(DDMiddleware(scheduler))'''


@deadline_router.message(F.text == 'Назначить/редактировать дедлайн')
async def add_deadlines(message: Message, state: FSMContext):
    await state.set_state(Deadline.name_deadline)
    await message.answer('Напиши название дедлайна, который хочешь создать.')


@deadline_router.message(Deadline.name_deadline)
async def dl_nm(message: Message, state: FSMContext):
    await state.update_data(name_deadline=message.text)
    await state.set_state(Deadline.day_deadline)
    await message.answer('Теперь введи дату и время дедлайна в формате день.месяц.год(два последних числа) час:минуты\nНапример, 01.01.31 13:00')


@deadline_router.message(F.text == 'да')
async def activate_deadlines(message: Message, apscheduler: AsyncIOScheduler, day_data, bot: Bot):
    '''await message.answer('Напоминания о дедлайнах успешно активированы. Теперь тебе будут приходить уведомления о приближающихся дедлайнах')'''
    day = datetime.datetime(int(day_data[2]), int(day_data[1]), int(day_data[0]), int(day_data[3]), int(day_data[4]))
    apscheduler.add_job(send_deadline, trigger='date', run_date = day, args = (message, bot,))


@deadline_router.message(Deadline.day_deadline)
async def dl_d(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler, bot: Bot):
    day = message.text
    if not check_data(day):
        await message.answer('Перепроверь правильность написания дедлайна по образцу выше.\nНапомним формат записи: день.месяц.год(два последних числа) час:минуты\nНапример, 01.01.31 13:00 ')
        await message.answer('Введите дату дедлайна в формате день.месяц.год')
        await state.set_state(Deadline.day_deadline)
    else:
        day_list = day.split(' ')
        day_data = day_list[0].split('.')
        day_time = day_list[1].split(':')
        data_deadline = await state.get_data()
        number_gr = await rq.get_group(message.from_user.id)
        await rq.set_deadline(name_deadline=data_deadline['name_deadline'], number_gr=number_gr,
        day=str(day_data[0]),  month=str(day_data[1]),
        year=str(day_data[2]), hour=str(day_time[0]), 
        minute=str(day_time[1])) 
        await activate_deadlines(message, apscheduler,  day_data+day_time, bot)
        await message.answer('Круто, дедлайн добавлен.')
        await message.answer('Что надо?',
                             reply_markup=await kb.main(message.from_user.id))




