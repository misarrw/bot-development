### Импорты
from aiogram import F, Router, Bot
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


### Импорты из файлов
import app.database.requests as rq
import app.keyboards as kb
from app.sup_func import check_data


class Deadline(StatesGroup):
    name_deadline = State()
    day_deadline = State()
    time_deadline = State()
    day = State()


deadline_router = Router()


@deadline_router.message(F.text == 'Назначить/редактировать дедлайн')
async def add_deadlines(message: Message, state: FSMContext):
    await state.set_state(Deadline.name_deadline)
    await message.answer('Напиши название дедлайна, который хочешь создать.')


@deadline_router.message(Deadline.name_deadline)
async def dl_nm(message: Message, state: FSMContext):
    await state.update_data(name_deadline=message.text)
    await state.set_state(Deadline.day_deadline)
    await message.answer('Теперь введи дату и время дедлайна в формате день.месяц.год час:минуты\nНапример, 01.01.2031 13:00')


@deadline_router.message(Deadline.day_deadline)
async def dl_d(message: Message, state: FSMContext, apscheduler: AsyncIOScheduler, bot: Bot):
    day = message.text
    try:
        if check_data(day):
            day_list = day.split(' ')
            day_data = day_list[0].split('.')
            day_time = day_list[1].split(':')
            data_deadline = await state.get_data()
            group = await rq.get_group(message.from_user.id)
            await rq.set_deadline(name_deadline=data_deadline['name_deadline'], group=group,
            day=day_data[0],  month=day_data[1],
            year=day_data[2], hour=day_time[0],
            minute=day_time[1])
            await activate_deadlines(message, apscheduler,  day_data, day_time, bot, data_deadline['name_deadline'])
            await message.answer('Круто, дедлайн добавлен.')
            await message.answer('Что надо?',
                                reply_markup=await kb.main(message.from_user.id))
        else:
            await message.answer('Дата неактуальна. Повтори попытку.\nНапомним формат записи: день.месяц.год час:минуты\nНапример, 01.01.2031 13:00 ')
            await message.answer('Введите дату дедлайна в формате день.месяц.год')
            await state.set_state(Deadline.day_deadline)
    except ValueError:
        await message.answer('Перепроверь правильность написания дедлайна по образцу выше.\nНапомним формат записи: день.месяц.год час:минуты\nНапример, 01.01.2031 13:00 ')
        await message.answer('Введите дату дедлайна в формате день.месяц.год')
        await state.set_state(Deadline.day_deadline)


async def activate_deadlines(message: Message, apscheduler: AsyncIOScheduler, day_data, day_time, bot: Bot, name):
    '''await message.answer('Напоминания о дедлайнах успешно активированы. Теперь тебе будут приходить уведомления о приближающихся дедлайнах')'''
    day = datetime.datetime(int(day_data[2]), int(day_data[1]), int(day_data[0]), int(day_time[0]), int(day_time[1]))
    apscheduler.add_job(send_deadline, trigger='date', run_date = day - datetime.timedelta(days = 7), args = (message, bot, '.'.join(day_data)+ ' ' + ':'.join(day_time), name,))
    apscheduler.add_job(send_deadline, trigger='date', run_date = day - datetime.timedelta(days = 3), args = (message, bot, '.'.join(day_data)+ ' ' + ':'.join(day_time), name,))
    apscheduler.add_job(send_deadline, trigger='date', run_date = day - datetime.timedelta(hours = 5), args = (message, bot, '.'.join(day_data)+ ' ' + ':'.join(day_time), name,))


async def send_deadline(message: Message, bot: Bot, date, name):
    users_list = await rq.get_users(message.from_user.id)
    for user in users_list:
        await bot.send_message(user.tg_id, f'Кажется, приближается время дедлайна\nНазвание дедлайна: {name}\nВремя дедлайна: {date}')


        















'''for deadline in deadlines:
            sorted_deadlines_list.append(deadline)
        for deadline in sorted_deadlines_list:
            b_message += f'{deadline.name_deadline}\n' + f'{deadline.day}.{deadline.month}.{deadline.year} ' + f'{deadline.hour}:{deadline.minute}\n'
            deadline_date = f'{deadline.day}.{deadline.month}.{deadline.year}'
            ''''''current_date = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M'))'''
'''current_date = datetime.datetime.now()
            await message.answer(b_message)
            b_message = 'Упс! Кажется, приближается время дедлайна!\n'''



