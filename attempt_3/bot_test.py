import pytest
from unittest.mock import AsyncMock
import unittest


import app.sup_func as sf
import app.handlers as h
import app.keyboards as kb

class BotTest(unittest.TestCase):
    def test_check_data__positive(self):
       date = ('08.12.2024 13:00')
       self.assertFalse(sf.check_data(date))

    def test_sup_func_negative(self):
        date = ('08.12.24 1:00')
        with pytest.raises(AssertionError):
            self.assertTrue(sf.check_data(date))





### Положительные тесты
@pytest.mark.asyncio
async def test_edit_data_positive():
    message = AsyncMock()
    await h.edit_data(message)
    message.answer.assert_called_with('Настройки для старост', 
                         reply_markup = kb.master_settings)


@pytest.mark.asyncio
async def test_groups_positive():
    message = AsyncMock()
    await h.groups(message)
    message.answer.assert_called_with('Choose your бибика', reply_markup=kb.groups)


@pytest.mark.asyncio
async def test_curricular_positive():
    message = AsyncMock()
    await h.curricular(message)
    message.answer.assert_called_with('Всё для тебя', reply_markup=kb.curricular)


@pytest.mark.asyncio
async def test_channels_positive():
    message = AsyncMock()
    await h.channels(message)
    message.answer.assert_called_with('Полезное из каналов', reply_markup=kb.channels)


@pytest.mark.asyncio
async def test_contacts_cmd_positive():
    message = AsyncMock()
    await h.contacts_cmd(message)
    message.answer.assert_called_with('Полезное из контактов', reply_markup=kb.contacts)



@pytest.mark.asyncio
async def test_contact1_positive():
    callback = AsyncMock()
    await h.contact1(callback)
    callback.message.answer.assert_called_with('Иванов Федор Ильич\nТелефон: +7 (985) 471-86-23; 15194\n Почта: fivanov@hse.ru')


@pytest.mark.asyncio
async def test_contact2_positive():
    callback = AsyncMock()
    await h.contact2(callback)
    callback.message.answer.assert_called_with('Павлова Татьяна Александровна\nТелефон: +7 (495) 772-95-90; 11093\n Почта: miem-office@hse.ru')


@pytest.mark.asyncio
async def test_contact3_positive():
    callback = AsyncMock()
    await h.contact3(callback)
    callback.message.answer.assert_called_with('Тестова Екатерина Алексеевна\nТелефон: +7 (495) 772-95-90; 15179\n Почта: miem-office@hse.ru')


@pytest.mark.asyncio
async def test_contact4_positive():
    callback = AsyncMock()
    await h.contact4(callback)
    callback.message.answer.assert_called_with('справочная\nТелефон: +7 (495) 771-32-32')



### Отрицательные тесты
@pytest.mark.asyncio
async def test_edit_data_negative():
    message = AsyncMock()
    await h.edit_data(message)
    with pytest.raises(AssertionError):
        message.answer.assert_called_with('Настройки для старост.', 
                         reply_markup = kb.master_settings)


@pytest.mark.asyncio
async def test_groups_negative():
    message = AsyncMock()
    await h.groups(message)
    with pytest.raises(AssertionError):
        message.answer.assert_called_with('Choose your бибика.', reply_markup=kb.groups)


@pytest.mark.asyncio
async def test_curricular_negative():
    message = AsyncMock()
    await h.curricular(message)
    with pytest.raises(AssertionError):
        message.answer.assert_called_with('Всё для тебя.', reply_markup=kb.curricular)


@pytest.mark.asyncio
async def test_channels_negative():
    message = AsyncMock()
    await h.channels(message)
    with pytest.raises(AssertionError):
        message.answer.assert_called_with('Полезное из каналов.', reply_markup=kb.channels)


@pytest.mark.asyncio
async def test_contacts_cmd_negative():
    message = AsyncMock()
    await h.contacts_cmd(message)
    with pytest.raises(AssertionError):
        message.answer.assert_called_with('Полезное из контактов.', reply_markup=kb.contacts)



@pytest.mark.asyncio
async def test_contact1_negative():
    callback = AsyncMock()
    await h.contact1(callback)
    with pytest.raises(AssertionError):
        callback.message.answer.assert_called_with('Иванов Федор Ильич\nТелефон: +7 (985) 471-86-23; 15194\n Почта: fivanov@hse.ru.')


@pytest.mark.asyncio
async def test_contact2_negative():
    callback = AsyncMock()
    await h.contact2(callback)
    with pytest.raises(AssertionError):
        callback.message.answer.assert_called_with('Павлова Татьяна Александровна\nТелефон: +7 (495) 772-95-90; 11093\n Почта: miem-office@hse.ru.')


@pytest.mark.asyncio
async def test_contact3_negative():
    callback = AsyncMock()
    await h.contact3(callback)
    with pytest.raises(AssertionError):
        callback.message.answer.assert_called_with('Тестова Екатерина Алексеевна\nТелефон: +7 (495) 772-95-90; 15179\n Почта: miem-office@hse.ru.')


@pytest.mark.asyncio
async def test_contact4_negative():
    callback = AsyncMock()
    await h.contact4(callback)
    with pytest.raises(AssertionError):
        callback.message.answer.assert_called_with('справочная\nТелефон: +7 (495) 771-32-32.')
    



