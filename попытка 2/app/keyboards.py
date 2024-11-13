from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, 
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=([
    [KeyboardButton(text='хочу учиться хочу учиться хочу учиться'), 
     KeyboardButton(text='если вайбы хоахоахоахоахоу')]]),
                            resize_keyboard=True,
                            input_field_placeholder='че надо-то?')

extracurricular = ReplyKeyboardMarkup(keyboard=([
    [KeyboardButton(text='инфофлуд')], 
    [KeyboardButton(text='если маме пожаловаться надо')],
    [KeyboardButton(text='хочу домой')]]),
                                resize_keyboard=True, 
                                input_field_placeholder='одобряем')

curricular = ReplyKeyboardMarkup(keyboard=([
    [KeyboardButton(text='расписаниееее'), 
     KeyboardButton(text='твои сокамерники. или не твои')],
     [KeyboardButton(text='хочу домой')]]), 
                                resize_keyboard=True, 
                                input_field_placeholder='лучше бы поехали на бибике')

groups = InlineKeyboardMarkup(inline_keyboard=
                   [[InlineKeyboardButton(text='б241иб', callback_data='241')],
                   [InlineKeyboardButton(text='б242иб', callback_data='242')],
                   [InlineKeyboardButton(text='б243иб', callback_data='243')],
                   [InlineKeyboardButton(text='б244иб', callback_data='244')],
                   [InlineKeyboardButton(text='б245иб', callback_data='245')]
                   ])

parents = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='мама бота', url='https://t.me/misarrw')]
    ])

channels = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='официальный канал ВШЭ', url='https://t.me/hse_official')],
    [InlineKeyboardButton(text='официальный канал МИЭМ', url='https://t.me/miem_hse')],
    [InlineKeyboardButton(text='канал с вакансиями', url='https://t.me/hsecareer')],
    [InlineKeyboardButton(text='канал СНТО', url='https://t.me/snto_miem')],
    [InlineKeyboardButton(text='ЭКСТРА', url='https://t.me/extrahse')],
    [InlineKeyboardButton(text='Movement', url='https://t.me/hse_movement')],
    [InlineKeyboardButton(text='афиша ВШЭ', url='https://t.me/HSEafisha')],
    [InlineKeyboardButton(text='обратная сторона BHS', url='https://t.me/bear_head_studio')],
    [InlineKeyboardButton(text='команда Уймина', url='https://t.me/au_team_news')],
    [InlineKeyboardButton(text='сплетни', url='https://t.me/inside_hse')]
])

contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Иванов (научрук)', callback_data='Иванов')],
    [InlineKeyboardButton(text='Павлова (менеджер)', callback_data='Павлова')],
    [InlineKeyboardButton(text='Тестова (менеджер)', callback_data='Тестова')],
    [InlineKeyboardButton(text='справочная', callback_data='справочная')],
    [InlineKeyboardButton(text='подразделение/работник', callback_data='п/р')],
    [InlineKeyboardButton(text='приемная комиссия', callback_data='прием.комиссия')]
])


reg_groups = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='б241иб'), KeyboardButton(text='б242иб')], 
    [KeyboardButton(text='б243иб'), KeyboardButton(text='б244иб'), KeyboardButton(text='б245иб')]
],
    resize_keyboard=True)

choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='yessss', callback_data='yes')],
    [InlineKeyboardButton(text='nnnoooo', callback_data='no')]
])

skip = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='скип')]
],
    resize_keyboard=True)

continue_= ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'продолжить')]
], resize_keyboard=True)