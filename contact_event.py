from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboard import chat_keyboard, welcome_keyboard
from config import TOKEN_SERVICE

import base


bot = None


class FSMChat(StatesGroup):
    chat = State()


#@dp.callback_query_handler(lambda c: c.data[0:c.data.find('#')] == 'contact', state=None)
async def process_contact_event(callback_query: types.CallbackQuery, state: FSMContext):
    all_events = await base.get_events()
    temp = callback_query.data
    idx = int(temp[temp.find('#')+1:len(temp)])
    await FSMChat.chat.set()
    async with state.proxy() as data:
        data['event_name'] = all_events[idx].event_name
        data['event_header'] = all_events[idx].event_header
        data['event_description'] = all_events[idx].event_description
        data['event_media'] = all_events[idx].event_media
        data['event_date'] = all_events[idx].event_date
        data['author_id'] = all_events[idx].author_id
        data['user_full_name'] = f'{callback_query.from_user.first_name} {callback_query.from_user.last_name}'
    await bot.send_message(callback_query.from_user.id, f'Вы вошли в чат с владельцем события {all_events[idx].event_name}', reply_markup = chat_keyboard)


#@dp.message_handler(lambda message: message.text == 'Посмотреть событие', state=FSMChat.chat)
async def process_view_event(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        text = data['event_header'] + '\n' + data['event_description']
        #await bot.send_photo(message.from_user.id, data['event_media'], caption=text)
        await send_event(message.from_user.id, data['event_media'], text)


#@dp.message_handler(lambda message: message.text == '❌Выйти из чата', state=FSMChat.chat)
async def process_exit_chat(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'Вы вышли из чата', reply_markup=welcome_keyboard)


#@dp.message_handler(state=FSMChat.chat)
async def process_get_message_from_chat(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        owner_chat_keyboard = InlineKeyboardMarkup()
        response_button_chat = InlineKeyboardButton('Ответить', callback_data=f'response#{message.from_user.id}#{message.from_user.first_name} {message.from_user.last_name}#'+data['event_name'])
        view_event_button = InlineKeyboardButton('Посмотреть событие',  url='t.me/tz_clientbot?start='+data['event_name'])
        owner_chat_keyboard.add(response_button_chat, view_event_button)
        
        with bot.with_token(TOKEN_SERVICE):
            caption_text = message.caption
            if message.text:
                text = '#Сообщение ' + data['event_name'] + '\n' + f'{message.from_user.first_name} {message.from_user.last_name}' + ': ' + message.text
                await bot.send_message(int(data['author_id']), text, reply_markup=owner_chat_keyboard)
            if message.photo:
                await bot.send_photo(int(data['author_id']), message.photo[0].file_id, caption=caption_text)
            if message.video:
                await bot.send_video(int(data['author_id']), message.video.file_id, caption=caption_text)
            if message.audio:
                await bot.send_audio(int(data['author_id']), message.audio.file_id, caption=caption_text)
            if message.voice:
                await bot.send_voice(int(data['author_id']), message.voice.file_id, caption=caption_text)
            if message.animation:
                await bot.send_animation(int(data['author_id']), message.animation.file_id, caption=caption_text)


#@dp.callback_query_handler(lambda c: c.data[0:c.data.find('#')] == 'response')
async def process_response_event(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMChat.chat.set()
    async with state.proxy() as data:
        data['first_id'] = callback_query.data.split('#')[1]
        data['first_fullname'] = callback_query.data.split('#')[2]
        data['event_name'] = callback_query.data.split('#')[3]
        data['author_id'] = callback_query.data.split('#')[1]
    await bot.send_message(callback_query.from_user.id, f'Вы вошли в чат с владельцем события ' + data['event_name'], reply_markup=chat_keyboard)


#@dp.callback_query_handler(lambda c: c.data[0:c.data.find('#')] == 'view')
async def process_show_event(callback_query: types.CallbackQuery, state: FSMContext):
    event = await base.get_event(callback_query.data.split('#')[1])
    text = f'{event.event_header}\n{event.event_description}'
    #await bot.send_photo(callback_query.from_user.id, event.event_media, caption=text)
    await send_event(callback_query.from_user.id, event.event_media, text)

#@dp.message_handler(commands=['start'], state='*' )
async def process_show_event_owner(message: types.Message, state: FSMContext):
    if message.get_args() == '':
        await bot.send_message(message.from_user.id, f'Добро пожаловать, {message.from_user.first_name} {message.from_user.last_name}', reply_markup=welcome_keyboard)
    else: 
        event = await base.get_event(message.get_args())
        await send_event(message.from_user.id, event.event_media, f'{event.event_header}\n{event.event_description}')


async def send_event(user_id, event_media, text):
    event_type = event_media.split('#')[0]
    event_media = event_media.split('#')[1]
    if event_type == 'photo':
        await bot.send_photo(user_id, event_media, caption=text)
    if event_type == 'video':
        await bot.send_video(user_id, event_media, caption=text)
    if event_type == 'audio':
        await bot.send_audio(user_id, event_media, caption=text)
    if event_type == 'animation':
        await bot.send_animation(user_id, event_media, caption=text)
    
 
def register_handlers_client(dp: Dispatcher, link_bot: Bot):
    global bot
    bot = link_bot
    dp.register_message_handler(process_show_event_owner, state='*', commands=['start'])
    dp.register_callback_query_handler(process_show_event, lambda c: c.data[0:c.data.find('#')] == 'view', state='*')
    dp.register_callback_query_handler(process_response_event, lambda c: c.data[0:c.data.find('#')] == 'response', state=None)
    dp.register_callback_query_handler(process_response_event, lambda c: c.data[0:c.data.find('#')] == 'response', state=FSMChat.chat)
    dp.register_callback_query_handler(process_contact_event, lambda c: c.data[0:c.data.find('#')] == 'contact', state=None)
    dp.register_callback_query_handler(process_contact_event, lambda c: c.data[0:c.data.find('#')] == 'contact', state=FSMChat.chat)
    dp.register_message_handler(process_view_event, lambda message: message.text == 'Посмотреть событие', state=FSMChat.chat)
    dp.register_message_handler(process_exit_chat, lambda message: message.text == '❌Выйти из чата', state=FSMChat.chat)
    dp.register_message_handler(process_get_message_from_chat, state=FSMChat.chat, content_types=['text', 'photo', 'video', 'voice', 'animation', 'audio'])

