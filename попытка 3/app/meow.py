from aiogram.types import Message, CallbackQuery
import datetime
from aiogram import Bot

import app.database.requests.requests as rq

async def send_deadline(message: Message, bot: Bot):
    users_list = await rq.get_users(message.from_user.id)
    for user in users_list:
        await bot.send_message(user.tg_id, 'kkk')
        deadlines = await rq.get_deadlines(message.from_user.id)
        sorted_deadlines_list = []
        b_message = 'Упс! Кажется, приближается время дедлайна!\n'
        for deadline in deadlines:
            sorted_deadlines_list.append(deadline)
        for deadline in sorted_deadlines_list:
            b_message += f'{deadline.name_deadline}\n' + f'{deadline.day}.{deadline.month}.{deadline.year} ' + f'{deadline.hour}:{deadline.minute}\n'
            deadline_date = f'{deadline.day}.{deadline.month}.{deadline.year}'
            '''current_date = str(datetime.datetime.now().strftime('%d.%m.%Y %H:%M'))'''
            current_date = datetime.datetime.now()
            if deadline_date == current_date:
                await message.answer(b_message)
            b_message = 'Упс! Кажется, приближается время дедлайна!\n'