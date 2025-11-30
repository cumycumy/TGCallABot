from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.strategy import FSMStrategy
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher

from asyncio import EventLoop
from os import environ
import logging

from . import routers


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = Bot(
	default=DefaultBotProperties(parse_mode=ParseMode.HTML),
	token=environ.get('TGCallABot'))
dispatcher = Dispatcher(
	storage=MemoryStorage(),
	fsm_strategy=FSMStrategy.USER_IN_CHAT)
dispatcher.include_router(routers.router)


async def bot_main(loop:EventLoop):
	logger.info('deleted webhooks with pending updates')
	await bot.delete_webhook(drop_pending_updates=True)

	await dispatcher.start_polling(
		bot,
		handle_as_tasks=True,
		tasks_concurrency_limit=40)