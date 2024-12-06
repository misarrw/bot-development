### Импорты
from aiogram import BaseMiddleware
import aiogram.dispatcher.middlewares 
from aiogram.types import TelegramObject
from aiogram.types import Message, CallbackQuery, User
from typing import Callable, Dict, Any, Awaitable
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler


### Импорты из файлов
import app.database.requests.requests as rq


### Инициализация логгера модуля
logger = logging.getLogger(__name__)


scheduler = AsyncIOScheduler()


### Реализация функции из файла 'requests.py'
async def get_status(message: Message):
    return await rq.get_user_status(message.from_user.id)

    
### Middleware для router
class PermissionMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        logger.debug('Вошли в %s', __class__.__name__)

        user = data.get('event_from_user')
        if user is not None:
            user_status = await rq.get_user_status(user.id)
            if user_status == True:
                logger.debug('Доступ к редактированию разрешен. ' + 
                            'Вышли из %s', __class__.__name__)
                return await handler(event, data)
            
        logger.debug('Доступ к редактированию запрещен. ' +
                    'Вышли из %s', __class__.__name__)

        return event.answer('Тебе недоступна эта функция.\n' + 
                            'Похоже, ты не староста')
    


### Middleware для advanced_router
class HandlerMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        logger.debug('Вошли в %s', __class__.__name__)

        result = await handler(event, data)
    
        logger.debug('Вышли из %s', __class__.__name__)

        return result
    

class DDMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        self._scheduler = scheduler

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:
    
        logger.debug('Вошли в %s', __class__.__name__)

        data['apscheduler'] = self._scheduler

        result = await handler(event, data)

        logger.debug('Вышли из %s', __class__.__name__)

        return result
        
'''class MasterHandlerMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        logger.debug('Вошли в %s', __class__.__name__)

        user = data.get('event_from_user')
        user_status = await rq.get_user_status(user.id)
        if user_status == 1:
            return await handler(event, data)
        
        logger.debug('Вышли из %s', __class__.__name__)
        return event.answer('Тебе недоступна эта функция.\n' + 
                            'Похоже, ты не староста :(')'''

        