from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboard import owner_chat_keyboard
from config import TOKEN_CLIENT
import base


bot = None


class FSMChat(StatesGroup):
    chat = State()


#@dp.callback_query_handler(lambda c: c.data[0:c.data.find('#')] == 'response', state=None)
async def process_contact_event(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMChat.chat.set()
    async with state.proxy() as data:
        data['first_id'] = callback_query.data.split('#')[1]
        data['first_fullname'] = callback_query.data.split('#')[2]
        data['event_name'] = callback_query.data.split('#')[3]
    await bot.send_message(callback_query.from_user.id, f'Вы вошли в чат с ' + callback_query.data.split('#')[2], reply_markup=owner_chat_keyboard)


#@dp.message_handler(lambda message: message.text == '❌Выйти из чата', state=FSMChat.chat)
async def process_exit_chat(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'Вы вышли из чата')


#@dp.message_handler(state=FSMChat.chat)
async def process_get_message_from_chat(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        with bot.with_token(TOKEN_CLIENT):
            text = 'Сообщение от владельца события ' + data['event_name'] + '\n' + message.text
            owner_chat_keyboard = InlineKeyboardMarkup()
            response_button_chat = InlineKeyboardButton('Ответить', callback_data=f'response#{message.from_user.id}#{message.from_user.first_name} {message.from_user.last_name}#'+data['event_name'])
            view_event_button = InlineKeyboardButton('Посмотреть событие', callback_data=f'view#'+data['event_name'])
            owner_chat_keyboard.add(response_button_chat, view_event_button)
            await bot.send_message(int(data['first_id']), text, reply_markup=owner_chat_keyboard)
 

def register_handlers_client(dp: Dispatcher, link_bot: Bot):
    global bot
    bot = link_bot
    dp.register_callback_query_handler(process_contact_event, lambda c: c.data[0:c.data.find('#')] == 'response', state=None)
    dp.register_callback_query_handler(process_contact_event, lambda c: c.data[0:c.data.find('#')] == 'response', state=FSMChat.chat)
    dp.register_message_handler(process_exit_chat, lambda message: message.text == '❌Выйти из чата', state=FSMChat.chat)
    dp.register_message_handler(process_get_message_from_chat, state=FSMChat.chat)
