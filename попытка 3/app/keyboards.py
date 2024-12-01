### Импорты
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, 
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from app.database.requests import check_status, get_subjects, get_users


### Стартовая клавиатура
async def main(tg_id):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text='Учебное'))
    keyboard.add(KeyboardButton(text='Внеучебное'))
    if await check_status(tg_id):
        keyboard.add(KeyboardButton(text='Редактирование данных'))
    return keyboard.adjust(1).as_markup()


### Редактирование данных
master_settings = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text = 'Редактировать расписание'), 
     KeyboardButton(text = 'Изменить список группы')], 
    [KeyboardButton(text = 'Отметить посещение'), 
     KeyboardButton(text = 'Назначить/редактировать дедлайн')],
    [KeyboardButton(text = 'Назад')]
], resize_keyboard = True, input_field_placeholder = 'Только для старост')


### Внеучебное
extracurricular = ReplyKeyboardMarkup(keyboard=([
    [KeyboardButton(text='Инфофлуд (телеграм-каналы)')], 
    [KeyboardButton(text='Если кому-то пожаловаться надо (контакты)')],
    [KeyboardButton(text='Назад')]]),
                                resize_keyboard=True, 
                                input_field_placeholder='не любим учиться,' +
                                'значит...')


### Учебное
curricular = ReplyKeyboardMarkup(keyboard = ([
    [KeyboardButton(text = 'Расписание'), 
     KeyboardButton(text = 'Список группы')], 
    [KeyboardButton(text = 'Посещение'), 
     KeyboardButton(text = 'Дедлайны')], 
    [KeyboardButton(text = 'Назад')]]), 
                    resize_keyboard = True, 
                    input_field_placeholder = 'кто любит учиться вообще???')


### Выбор группы
groups = InlineKeyboardMarkup(inline_keyboard=
                   [[InlineKeyboardButton(text='б241иб', 
                                          callback_data='241')],
                   [InlineKeyboardButton(text='б242иб', 
                                         callback_data='242')],
                   [InlineKeyboardButton(text='б243иб', 
                                         callback_data='243')],
                   [InlineKeyboardButton(text='б244иб', 
                                         callback_data='244')],
                   [InlineKeyboardButton(text='б245иб', 
                                         callback_data='245')]
                   ])


### Инлайн клавиатура с ссылками на телеграмы создателей
parents = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text = 'Мама бота', url = 'https://t.me/misarrw')], 
    [InlineKeyboardButton(text = 'Папа бота', url = 'https://t.me/jabohka')]
])


### Каналы
channels = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Официальный канал ВШЭ', 
                          url='https://t.me/hse_official')],
    [InlineKeyboardButton(text='Официальный канал МИЭМ', 
                          url='https://t.me/miem_hse')],
    [InlineKeyboardButton(text='Канал с вакансиями', 
                          url='https://t.me/hsecareer')],
    [InlineKeyboardButton(text='Канал СНТО', 
                          url='https://t.me/snto_miem')],
    [InlineKeyboardButton(text='ЭКСТРА', 
                          url='https://t.me/extrahse')],
    [InlineKeyboardButton(text='Movement', 
                          url='https://t.me/hse_movement')],
    [InlineKeyboardButton(text='Афиша ВШЭ', 
                          url='https://t.me/HSEafisha')],
    [InlineKeyboardButton(text='Обратная сторона BHS', 
                          url='https://t.me/bear_head_studio')],
    [InlineKeyboardButton(text='Команда Уймина', 
                          url='https://t.me/au_team_news')],
    [InlineKeyboardButton(text='Сплетни', 
                          url='https://t.me/inside_hse')]
])


### Контакты
contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Иванов (научрук)', 
                          callback_data='Иванов')],
    [InlineKeyboardButton(text='Павлова (менеджер)', 
                          callback_data='Павлова')],
    [InlineKeyboardButton(text='Тестова (менеджер)', 
                          callback_data='Тестова')],
    [InlineKeyboardButton(text='Справочная', 
                          callback_data='справочная')],
    [InlineKeyboardButton(text='Подразделение/работник', 
                          callback_data='п/р')],
    [InlineKeyboardButton(text='Приемная комиссия', 
                          callback_data='прием.комиссия')]
])


### Выбор группы при регистрации
reg_groups = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='б241иб'), KeyboardButton(text='б242иб')], 
    [KeyboardButton(text='б243иб'), KeyboardButton(text='б244иб'), KeyboardButton(text='б245иб')]
],
    resize_keyboard=True)


### Да/нет-ка (вроде бесполезно)
choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='yessss', callback_data='yes')],
    [InlineKeyboardButton(text='nnnoooo', callback_data='no')]
])


### Назад (пропуск действия)
skip = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='скип')]
],
    resize_keyboard=True)


### Продоложить
continue_= ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'продолжить')]
], resize_keyboard=True)


async def students(tg_id):
    keyboard = ReplyKeyboardBuilder()
    all_name = await get_users(tg_id)
    keyboard.add(KeyboardButton(text='ВСЁ!'))
    names_list = []
    for name in all_name:
        names_list.append(name.name_user)
    sorted_name_list = sorted(names_list)
    for name in sorted_name_list:
        keyboard.add(KeyboardButton(text=name))
    return keyboard.adjust(3).as_markup()


async def subjects():
    keyboard = ReplyKeyboardBuilder()
    all_subjects = await get_subjects()
    subjects_list = []
    for subject in all_subjects:
        subjects_list.append(subject.name_object)
    sorted_subject_list = sorted(subjects_list)
    for subject in sorted_subject_list:
        keyboard.add(KeyboardButton(text=subject))
    keyboard.add(KeyboardButton(text='Добавить предмет'))
    return keyboard.adjust(2).as_markup()

add_subjects = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Всё!')]
], resize_keyboard=True)