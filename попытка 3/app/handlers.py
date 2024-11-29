### Импорты
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

### Импорты из файлов
import app.database.requests as rq
import app.keyboards as kb
from app.middlewares import HandlerMiddleware


### Этапы регистрации
class Reg(StatesGroup):
    group = State()
    status = State()
    password = State()
    name = State()


### Подключение роутеров
router = Router()


### Подключение Middleware
router.message.outer_middleware(HandlerMiddleware())


### Ввод переменных
c = 0


### стартовая команда
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Кчау... Я твоя бибика. Чем смогу, помогу')
    if await rq.set_user_id(message.from_user.id) == False:
        await message.answer('Но мы с тобой не знакомы пока,\nтак что ' + 
                             'расскажи мне, кто ты')
        await state.set_state(Reg.group)
        await message.answer('Выбери свою бибику (группу)',
                         reply_markup=kb.reg_groups)
    else:
        await message.answer('Что надо?', reply_markup=kb.main)


### регистрация
@router.message(Reg.group)
async def reg_gr(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await state.set_state(Reg.password)
    await message.answer('Окей, если ты (зам)староста, введи пароль:',
                         reply_markup=kb.skip)


@router.message(Reg.password)
async def check_password(message: Message, state: FSMContext):
    global c
    data_intrm_group = await state.get_data()
    if message.text == 'скип':
        await state.update_data(password=message.text)
        await state.set_state(Reg.status)
    else:
        check = await rq.check_password(data_intrm_group['group'], message.text)
        if check:
            await state.update_data(password=message.text)
            await state.set_state(Reg.status)
            await message.answer('Верю')
        elif not check and c < 3:
            c += 1
            await state.update_data(password=message.text)
            await state.set_state(Reg.password)
            await message.answer(f'Пароль не такой!. Еще {3-c} попытки/а')
        elif c == 3:
            await state.set_state(Reg.status)
            await message.answer('Не верю')
    await message.answer('Давай знакомиться. Введи свои имя и фамилию')


@router.message(Reg.status)
async def reg_st(message: Message, state: FSMContext):
    data_intrm_group = await state.get_data()
    check = await rq.check_password(data_intrm_group['group'], data_intrm_group['password'])
    if not check:
        await state.update_data(status=False)
    else:
        await state.update_data(status=True)
    await state.set_state(Reg.name)
    await state.update_data(name = message.text)
    data_reg = await state.get_data()
    await rq.set_user(data_reg['name'], message.from_user.id, data_reg['group'], data_reg['status'])
    await state.clear()
    await message.answer('Вроде зарегистрировались.\nЧто надо?',
                         reply_markup = kb.main)


### Расписание
@router.message(F.text == 'Расписание')
async def get_schedule(message: Message):
    await message.answer('Держи расписание своей группы')
    schedule = await rq.get_schedule(message.from_user.id)
    for i in schedule:
        await message.answer(f'Понедельник:\n{i.monday}\nВторник:\n' + 
                             f'{i.tuesday}\n' +
                             f'Среда:\n{i.wednesday}\nЧетверг:\n' + 
                             f'{i.thursday}\n' +
                             f'Пятница:\n{i.friday}\nСуббота:\n{i.saturday}\n')


### Опции для старост
@router.message(F.text == 'Редактирование данных')
async def edit_data(message: Message):
    await message.answer('Настройки для старост', 
                         reply_markup = kb.master_settings)


### Команда /help (она бесполезная)
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('S O S please some-one-help-me')


### Список группы
@router.message(F.text == 'Список группы')
async def groups(message: Message):
    await message.answer('Choose your бибика', reply_markup=kb.groups)


### Учебное
@router.message(F.text == 'Учебное')
async def curricular(message: Message):
    await message.answer('Всё для тебя', reply_markup=kb.curricular)


### Внеучебное
@router.message(F.text == 'Внеучебное')
async def extracurricular(message: Message):
    await message.answer('Все для тебя', reply_markup=kb.extracurricular)


### Телеграм-каналы
@router.message(F.text == 'Инфофлуд (телеграм-каналы)')
async def channels(message: Message):
    await message.answer('Полезное из каналов', reply_markup=kb.channels)


### Контакты
@router.message(F.text == 'Если кому-то пожаловаться надо (контакты)')
async def contacts_cmd(message: Message):
    await message.answer('Полезное из контактов', reply_markup=kb.contacts)


### Назад
@router.message(F.text == 'Назад')
async def back_cmd(message: Message):
    await message.answer('Ну и пожалуйста', reply_markup=kb.main)


### Контакты (конкретно)
@router.callback_query(F.data == 'Иванов')
async def contact1(callback: CallbackQuery):
    await callback.message.answer('Иванов Федор Ильич\nТелефон: +7 (985) 471-86-23; 15194\n Почта: fivanov@hse.ru')

@router.callback_query(F.data == 'Павлова')
async def contact2(callback: CallbackQuery):
    await callback.message.answer('Павлова Татьяна Александровна\nТелефон: +7 (495) 772-95-90; 11093\n Почта: miem-office@hse.ru')

@router.callback_query(F.data == 'Тестова')
async def contact3(callback: CallbackQuery):
    await callback.message.answer('Тестова Екатерина Алексеевна\nТелефон: +7 (495) 772-95-90; 15179\n Почта: miem-office@hse.ru')

@router.callback_query(F.data == 'Справочная')
async def contact4(callback: CallbackQuery):
    await callback.message.answer('справочная\nТелефон: +7 (495) 771-32-32')

@router.callback_query(F.data == 'П/р')
async def contact5(callback: CallbackQuery):
    await callback.message.answer('для соединения с подразделением/работником\nТелефон: +7 (495) 531-00-00')

@router.callback_query(F.data == 'Прием.комиссия')
async def contact6(callback: CallbackQuery):
    await callback.message.answer('приемная комиссия\nТелефон: (495) 771-32-42; (495) 916-88-44')



'''@router.callback_query(F.data == '241')'''
'''async def group241(callback: CallbackQuery):'''
'''    await callback.message.answer('б241иб')'''

'''@router.callback_query(F.data == '242')'''
'''async def group241(callback: CallbackQuery):'''
'''    await callback.message.answer('б242иб')'''

'''@router.callback_query(F.data == '243')'''
'''async def group241(callback: CallbackQuery):'''
'''    await callback.message.answer('б243иб')'''

'''@router.callback_query(F.data == '244')'''
'''async def group241(callback: CallbackQuery):'''
'''    await callback.message.answer('б244иб')'''

'''@router.callback_query(F.data == '245')'''
'''async def group241(callback: CallbackQuery):'''
'''    await callback.message.answer('б245иб')'''



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
