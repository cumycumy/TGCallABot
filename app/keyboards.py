from aiogram.utils.keyboard import InlineKeyboardBuilder


keyboard = (InlineKeyboardBuilder()
	.button(text='Остановить', callback_data='cancel')
).as_markup()