from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from ollama import AsyncClient
from os import environ
import time

from . import keyboards
from . import model


router = Router()


scheduler = AsyncIOScheduler()

client = AsyncClient(
	host='https://ollama.com',
	headers={
		'Authorization': ('Bearer ' + environ.get('DEEPSEEK', '')),
	},
)
chat = model.Chat(
	model.Message('system',
		'Ты должен ответить на все вопросы пользователя!'),
)

messages = {}


@router.message()
async def message(message: Message):
	messages.setdefault(message.from_user.id, dict())

	answer = await message.reply(
		'Генерация...',
		reply_markup=keyboards.keyboard)
	reply = {
		'run': True,
		'text': str(),
	}
	messages[message.from_user.id].setdefault(
		answer.message_id, reply)

	chat.add(model.Message('user', message.text))

	writed = False
	think = False
	start_time = end_time = time.time()
	async for part in await client.chat(
			model='deepseek-v3.1:671b-cloud',
			messages=chat.messages,
			stream=True,
			think=True):
		if not reply['run']: break
		if not writed:
			start_time = time.time()
			writed = True

		if part.message.thinking:
			if not think:
				think = True
				reply['text'] += '=' * 10
				reply['text'] += ' Мышление '
				reply['text'] += '=' * 10
				reply['text'] += '\n'
			reply['text'] += part.message.thinking
		else:
			if think:
				think = False
				reply['text'] += '\n'
				reply['text'] += '=' * 10
				reply['text'] +=' Мышление '
				reply['text'] += '=' * 10
				reply['text'] += '\n'
			reply['text'] += part.message.content
		end_time = time.time()
		if (end_time - start_time) >= 1:
			try:
				await answer.edit_text(
					text=reply['text'],
					reply_markup=keyboards.keyboard)
			except TelegramBadRequest as error:
				print(error)
			writed = False

	chat.add(model.Message('assistant', reply['text']))
	del messages[message.from_user.id][answer.message_id]


@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery):
	reply = messages[callback.from_user.id][callback.message.message_id]

	reply['text'] += '\n'
	reply['text'] += '=' * 10
	reply['text'] += ' Отмена '
	reply['text'] += '=' * 10

	reply['run'] = False
	
	await callback.message.edit_text(text=reply['text'])