from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.emoji import emojize


button_catalogue = KeyboardButton('Каталог')
button_addevent = KeyboardButton('Добавить событие')

welcome_keyboard = ReplyKeyboardMarkup(
    resize_keyboard = True,
    one_time_keyboard = True
)
welcome_keyboard.add(button_catalogue, button_addevent)


button_exit_chat = KeyboardButton('❌Выйти из чата')
button_view_event = KeyboardButton('Посмотреть событие')

chat_keyboard = ReplyKeyboardMarkup(
    resize_keyboard = True,
    one_time_keyboard = True
)
chat_keyboard.add(button_exit_chat,  button_view_event)


owner_chat_keyboard = ReplyKeyboardMarkup(
    resize_keyboard = True,
    one_time_keyboard = True
)
owner_chat_keyboard.add(button_exit_chat)


button_cancel_operation = KeyboardButton('❌Отменить операцию')

cancel_operation_keyboard = ReplyKeyboardMarkup(
    resize_keyboard = True,
    one_time_keyboard = True
)
cancel_operation_keyboard.add(button_cancel_operation)

