from aiogram.types import Message, CallbackQuery
from aiogram import Router

from ollama import AsyncClient

from os import environ

from . import keyboards
from . import model


router = Router()


client = AsyncClient(
	headers={
		'Authorization': ('Bearer ' + environ.get('DEEPSEEK', '')),
	},
)

chat = model.Chat(
	model.Message('system',
		'Ты должен ответить на все вопросы пользователя!'),
)


can_generate = True

@router.message()
async def message(message: Message):
	chat.add(model.Message('user', message.text))

	text = []
	think = False
	async for part in await client.chat(
			model='deepseek-v3.1:671b-cloud',
			messages=chat.messages,
			stream=True,
			think=True):
		if not can_generate:
			break
		if part.message.thinking:
			if not think:
				think = True
				text.append('=' * 10)
				text.append(' Мышление ')
				text.append('=' * 10)
				text.append('\n')
			text.append(part.message.thinking)
		else:
			if think:
				think = False
				text.append('\n')
				text.append('=' * 10)
				text.append(' Мышление ')
				text.append('=' * 10)
				text.append('\n')
			text.append(part.message.content)
	text = ''.join(text)
	chat.add(model.Message('assistant', text))
	await message.reply(text, reply_markup=keyboards.keyboard)


@router.callback_query(F.data == 'cancel')
async def cancel(callback: CallbackQuery):
	can_generate = False

	await callback.message.edit_markup(reply_markup=None)