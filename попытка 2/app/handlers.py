from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import app.database.requests as rq

import app.keyboards as kb

class Register(StatesGroup):
    group = State()
    status = State() # посмотри, что такое классы
    password = State()

router = Router()
с = 0

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('иу, тебе тоже про меня рассказали...\nменя зовут... а, впрочем, неважно.\nчто надо?.', reply_markup=kb.parents)
    if await rq.set_user_id(message.from_user.id) == False:
        await message.answer('продолжим с регистрацией?', reply_markup=kb.choice)
    else:
        await message.answer('ты можешь получить доступ к личной инфе')

@router.callback_query(F.data == 'yes')
async def register(callback: CallbackQuery):
    await callback.message.answer('еее, давай зарегаемся!')
    await callback.state.set_state(Register.group)
    await callback.message.answer('choose your бибика', reply_markup=kb.groups)

@router.message(Register.group)
async def register_group(message: Message, state: FSMContext):
    await state.update_data(group = message.text)
    await state.set_state(Register.password)
    await message.answer('окей. введи пароль, если ты (зам)староста', reply_markup=kb.skip)

@router.message(Register.password)
async def check_password(message: Message, state: FSMContext):
    global c
    data_interim_group = await state.get_data()
    if message.text == 'нет, скип':
        await state.update_data(password = message.text)
        await state.set_state(Register.status)
    else:
        check = await rq.check_password(data_interim_group['group'], message.text)
        if check:
           await state.update_data(password=message.text)
           await state.set_state(Register.status)
           await message.answer('верю')
        elif not check and c<3:
           c+=1
           await state.update_data(password=message.text)
           await state.set_state(Register.password)
           await message.answer(f'неправильно. еще {3-c} попытки')
        elif c==3:
            await state.set_state(Register.status)
            await message.answer('не верю')
            await message.answer('нажми, чтобы продолжить',
                        reply_markup=kb.continue_)
        if check:
           await state.update_data(password=message.text)
           await state.set_state(Register.status)
           await message.answer('верю')
        elif not check and c<3:
           c+=1
           await state.update_data(password=message.text)
           await state.set_state(Register.password)
           await message.answer(f'неправильно. еще {3-c} попытки')
        elif c==3:
            await state.set_state(Register.status)
            await message.answer('не верю')
            await message.answer('нажми, чтобы продолжить',
                        reply_markup=kb.continue_)

@router.message(Register.status)
async def reg_st(message: Message, state: FSMContext):
    data_interim_group=await state.get_data()
    check=await rq.check_password(data_interim_group['group'],data_interim_group['password'])
    if not(check):
        await state.update_data(status=False)
    else:
        await state.update_data(status=True)
    data_reg=await state.get_data()
    await rq.set_user(data_reg['group'], message.from_user.id, data_reg['status'])
    await message.answer('поехалииииии')

@router.callback_query(F.data == 'no')
async def yes(callback: CallbackQuery):
    await callback.message.answer('ну ок', reply_markup=kb.main)

@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('S O S please some-one-help-me')

@router.message(F.text == 'твои сокамерники. или не твои')
async def groups(message: Message):
    await message.answer('choose your бибика', reply_markup=kb.groups)

@router.message(F.text == 'хочу учиться хочу учиться хочу учиться')
async def curricular(message: Message):
    await message.answer('осуждаем', reply_markup=kb.curricular)

@router.message(F.text == 'если вайбы хоахоахоахоахоу')
async def extracurricular(message: Message):
    await message.answer('ураураура не будем учиться', reply_markup=kb.extracurricular)

@router.message(F.text == 'инфофлуд')
async def channels(message: Message):
    await message.answer('полезное из каналов', reply_markup=kb.channels)

@router.message(F.text == 'если маме пожаловаться надо')
async def contacts_cmd(message: Message):
    await message.answer('полезное из контактов', reply_markup=kb.contacts)

@router.message(F.text == 'хочу домой')
async def back_cmd(message: Message):
    await message.answer('я тоже, если честно', reply_markup=kb.main)


@router.callback_query(F.data == 'Иванов')
async def contact1(callback: CallbackQuery):
    await callback.message.answer('Иванов Федор Ильич\nТелефон: +7 (985) 471-86-23; 15194\n Почта: fivanov@hse.ru')

@router.callback_query(F.data == 'Павлова')
async def contact2(callback: CallbackQuery):
    await callback.message.answer('Павлова Татьяна Александровна\nТелефон: +7 (495) 772-95-90; 11093\n Почта: miem-office@hse.ru')

@router.callback_query(F.data == 'Тестова')
async def contact3(callback: CallbackQuery):
    await callback.message.answer('Тестова Екатерина Алексеевна\nТелефон: +7 (495) 772-95-90; 15179\n Почта: miem-office@hse.ru')

@router.callback_query(F.data == 'справочная')
async def contact4(callback: CallbackQuery):
    await callback.message.answer('справочная\nТелефон: +7 (495) 771-32-32')

@router.callback_query(F.data == 'п/р')
async def contact5(callback: CallbackQuery):
    await callback.message.answer('для соединения с подразделением/работником\nТелефон: +7 (495) 531-00-00')

@router.callback_query(F.data == 'прием.комиссия')
async def contact6(callback: CallbackQuery):
    await callback.message.answer('приемная комиссия\nТелефон: (495) 771-32-42; (495) 916-88-44')



@router.callback_query(F.data == '241')
async def group241(callback: CallbackQuery):
    await callback.message.answer('б241иб')

@router.callback_query(F.data == '242')
async def group241(callback: CallbackQuery):
    await callback.message.answer('б242иб')

@router.callback_query(F.data == '243')
async def group241(callback: CallbackQuery):
    await callback.message.answer('б243иб')

@router.callback_query(F.data == '244')
async def group241(callback: CallbackQuery):
    await callback.message.answer('б244иб')

@router.callback_query(F.data == '245')
async def group241(callback: CallbackQuery):
    await callback.message.answer('б245иб')



'''@router.message(Command('register'))'''
'''async def register(message: Message, state: FSMContext):'''
'''    await state.set_state(Register.name)'''
'''    await message.answer('кто ты есть?')'''

'''@router.message(Register.name)'''
'''async def register_name(message: Message, state: FSMContext):'''
'''    await state.update_data(name=message.text)'''
'''    await state.set_state(Register.surname)'''
'''    await message.answer('а по фамилии?')'''

'''@router.message(Register.surname)'''
'''async def register_surname(message: Message, state: FSMContext):'''
'''    await state.update_data(surname=message.text)'''
'''    data = await state.get_data()'''
'''    await message.answer(f'перепроверь машину\nимя: {data["name"]}\nфамилия: {data["surname"]}')'''
### команда вверху вынимает значения
'''    await state.clear()'''
### команда сверху чистит записанные данные, чтобы бот не засорялся





# пример команды, чтобы запросить номер телефона
'''get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер','''
'''                                                           request_contact=True)]])''' 
