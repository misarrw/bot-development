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
from app.sup_func import check_data


### Этапы регистрации
class Reg(StatesGroup):
    group = State()
    status = State()
    password = State()
    name = State()

class Absent(StatesGroup):
    back_home = State()
    name_subject = State()
    name_user = State()

class Subjects(StatesGroup):
    subject = State()
    subject_skip = State()


### иные классы
class Deadline(StatesGroup):
    name_deadline = State()
    day_deadline = State()
    time_deadline = State()


### Подключение роутеров
router = Router()


### Подключение Middleware
router.message.outer_middleware(HandlerMiddleware())


### Ввод переменных
itr_password = 0
tab = ' '*8


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
    global itr_password
    intermediate_data = await state.get_data()
    if message.text == 'скип':
        await state.update_data(password=message.text)
        await state.set_state(Reg.status)
        await message.answer('Давай знакомиться. Введи свои имя и фамилию')
    else:
        check = await rq.check_password(intermediate_data['group'], message.text)
        if check:
            await state.update_data(password=message.text)
            await state.set_state(Reg.status)
            await message.answer('Верю')
            await message.answer('Давай знакомиться. Введи свои имя и фамилию')
        elif not check and itr_password < 3:
            itr_password += 1
            await state.update_data(password=message.text)
            await state.set_state(Reg.password)
            await message.answer(f'Пароль не такой!. Еще {3-itr_password} попытки/а')
        elif itr_password == 3:
            await state.set_state(Reg.status)
            await message.answer('Не верю')
            await message.answer('Давай знакомиться. Введи свои имя и фамилию')


@router.message(Reg.status)
async def reg_st(message: Message, state: FSMContext):
    intermediate_data = await state.get_data()
    check = await rq.check_password(intermediate_data['group'], intermediate_data['password'])
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
    await message.answer('Ну и пожалуйста', reply_markup= await kb.main(message.from_user.id))


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






@router.message(Absent.back_home)
@router.message(F.text == 'Отметить посещение')
async def pick_subject(message: Message, state: FSMContext):
    await message.answer('Выбери предмет',
                         reply_markup=await kb.subjects())
    await state.set_state(Absent.name_subject)


@router.message(Absent.name_subject)
async def pick_subject2(message: Message, state: FSMContext):
    if message.text == 'Добавить предмет':
        await state.clear()
        await state.set_state(Subjects.subject)
        await message.answer('Напиши название предмета, если хочешь добавить несколько, вводи в разных сообщения',
                             reply_markup=kb.add_subjects)
    else:
        await state.update_data(name_subject=message.text)
        await message.answer('Выбери студентов',
                             reply_markup=await kb.students(message.from_user.id))
        await state.set_state(Absent.name_user)


@router.message(Absent.name_user)
async def mark_absent(message: Message, state: FSMContext):
    if message.text == 'ВСЁ!':
        await state.clear()
        await message.answer('Чем могу помочь?',
                             reply_markup=await kb.main(message.from_user.id))
    else:
        number_group = await rq.get_group(message.from_user.id)
        if not await rq.check_student(message.text, *number_group):
            await message.answer('Ошибка, студент не найден.')
        else:
            await state.update_data(name_user=message.text)
            data_mark = await state.get_data()
            await rq.set_absent(name_user=data_mark['name_user'], number_group=number_group[0],
                                name_object=data_mark['name_subject'])
        await state.set_state(Absent.name_user)


@router.message(Subjects.subject)
async def add_subject(message: Message, state: FSMContext):
    if message.text == 'Всё!':
        await message.answer('Выбери предмет',
                             reply_markup=await kb.subjects())
        await state.clear()
        await state.set_state(Absent.back_home)
    elif not await rq.add_subject(message.text):
        await message.answer('Ошибка, предмет уже существует!')
        await state.set_state(Subjects.subject)


@router.message(F.text == 'Пропуски')
async def pick_subject_skip(message: Message, state: FSMContext):
    await message.answer('Выберите предмет',
                         reply_markup=await kb.subjects())
    await state.set_state(Subjects.subject_skip)


@router.message(Subjects.subject_skip)
async def print_table_skips(message: Message):
    sorted_absents_list = await rq.get_absents(message.from_user.id)
    ending_str = f'Пропуски предмета {message.text}\n'
    for absent in sorted_absents_list:
        cnt_gap = await rq.get_cnt_gap(absent)
        ending_str += f'{absent} - {cnt_gap} пропуска\n'
    await message.answer(ending_str)



@router.message(F.text == 'Просмотреть дедлайны')
async def begin_deadlines(message: Message):
    global tab
    deadlines = await rq.get_deadlines(message.from_user.id)
    sorted_deadlines_list = []
    b_message = 'Дедлайн:'+tab*2+'Срок:\n'
    for deadline in deadlines:
        sorted_deadlines_list.append(deadline)
    sorted_deadlines_list = sorted(sorted_deadlines_list)
    for deadline in sorted_deadlines_list:
        b_message += f'{deadline.name_deadline}'+tab+f'{deadline.day_deadline} {deadline.time_deadline}\n'
        print(b_message)
    await message.answer(b_message,
                         reply_markup=await kb.main(message.from_user.id))


@router.message(F.text == 'Назначить/редактировать дедлайн')
async def add_deadlines(message: Message, state: FSMContext):
    await state.set_state(Deadline.name_deadline)
    await message.answer('Давай начнем с названия дедлайна')


@router.message(Deadline.name_deadline)
async def dl_nm(message: Message, state: FSMContext):
    await state.update_data(name_deadline=message.text)
    await state.set_state(Deadline.day_deadline)
    await message.answer('Теперь введи дату и время дедлайна в формате день.месяц.год(два последних числа) час:минуты')


@router.message(Deadline.day_deadline)
async def dl_d(message: Message, state: FSMContext):
    day = message.text
    if not check_data(day):
        await message.answer('Ошибка! Неверный формат или время дедлайна уже истекло')
        await message.answer('Введите дату дедлайна в формате день.месяц.год')
        await state.set_state(Deadline.day_deadline)
    else:
        day_list = day.split(' ')
        await state.update_data(day_deadline=day_list[0])
        await state.update_data(time_deadline=day_list[1])
        data_deadline = await state.get_data()
        number_gr = await rq.get_group(message.from_user.id)
        await rq.set_deadline(name_deadline=data_deadline['name_deadline'], number_gr=number_gr,
                              day_deadline=data_deadline['day_deadline'], time_deadline=data_deadline['time_deadline'])
        await state.clear()
        await message.answer('Дедлайн добавлен!')
        await message.answer('Чем могу помочь?',
                             reply_markup=await kb.main(message.from_user.id))

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
