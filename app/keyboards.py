from aiogram.utils.keyboarb import InlineKeyboardBuilder


keyboard = (InlineKeyboardBuilder()
	.button(text='Остановить', callback_data='cancel')
).as_markup()