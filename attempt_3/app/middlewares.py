### Импорты
from aiogram import BaseMiddleware
import aiogram.dispatcher.middlewares 
from aiogram.types import TelegramObject
from aiogram.types import Message, CallbackQuery, User
from typing import Callable, Dict, Any, Awaitable
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler


### Импорты из файлов
from app.database.requests import check_status


### Инициализация логгера модуля
logger = logging.getLogger(__name__)


scheduler = AsyncIOScheduler()


class DDMiddleware(BaseMiddleware):
    """Класс мидлвэйр, отвечающий за дедлайны"""
    def __init__(self, scheduler: AsyncIOScheduler) -> None:
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


class PermissionMiddleware(BaseMiddleware):
    """Класс мидлвэйр, отвечающий за проверку разрешения использования некоторых функций"""
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        logger.debug('Вошли в %s', __class__.__name__)

        user = data.get('event_from_user')
        if user is not None:
            user_status = await check_status(user.id)
            if user_status:
                logger.debug('Доступ к редактированию разрешен. ' + 
                            'Вышли из %s', __class__.__name__)
                return await handler(event, data)
            
        logger.debug('Доступ к редактированию запрещен. ' +
                    'Вышли из %s', __class__.__name__)

        return event.answer('Тебе недоступна эта функция.\n' + 
                            'Похоже, ты не староста')
