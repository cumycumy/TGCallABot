from aiogram.types import Message
from aiogram import Router

from ollama import AsyncClient

from os import environ

from . import model


router = Router()


client = AsyncClient(
	headers={
		'Authorization': ('Bearer ' + environ.get('deepseek', '')),
	},
)

chat = model.Chat(
	model.Message('system',
		'Ты должен ответить на все вопросы пользователя!'),
)


@router.message()
async def message(message: Message):
	chat.add(model.Message('user', message.text))

	text = '+'
	think = False
	async for part in await client.chat(
			model='deepseek-v3.1:671b-cloud',
			messages=chat.messages,
			stream=True,
			think=True):
		if part.message.thinking:
			if not think:
				think = True
				text += '=' * 10 + ' Мышление ' + '=' * 10 + '\n'
			text += part.message.thinking
		else:
			if think:
				think = False
				text += '\n'
				text += '=' * 10 + ' Разговор ' + '=' * 10 + '\n'
			text += part.message.content
	
	chat.add(model.Message('assistant', text))
	await message.answer(text)