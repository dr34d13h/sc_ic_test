from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, types, Dispatcher
from aiogram.utils.emoji import emojize
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboard import chat_keyboard, welcome_keyboard
import base


bot = None


#@dp.message_handler(lambda message: message.text == 'Каталог', state=None)
async def process_get_catalogue(message: types.Message):
    all_events = await base.get_events()
    await send_event_with_keyboard(message.from_user.id, 0, all_events, 2)


#@dp.callback_query_handler(func = lambda c: c.data[0:c.data.find('#')] == 'delete')
async def process_callback_delete_event(callback_query: types.CallbackQuery):
    temp = callback_query.data
    idx = int(temp[temp.find('#')+1:len(temp)])
    delete_check_keyboard = InlineKeyboardMarkup()
    button_true_event = InlineKeyboardButton('✅Да', callback_data=f'confirmdelete#{idx}')
    button_false_event = InlineKeyboardButton('❌Нет', callback_data=f'canceldelete#{idx}')
    delete_check_keyboard.add(button_true_event, button_false_event)
    await bot.send_message(callback_query.from_user.id, 'Вы действительно хотите удалить это событие?', reply_markup=delete_check_keyboard, reply_to_message_id=callback_query.message.message_id)


#@dp.callback_query_handler(lambda c: c.data[0:c.data.find('#')] == 'one')
async def process_callback_pagination_one(callback_query: types.CallbackQuery):
    all_events = await base.get_events()
    temp = callback_query.data
    await send_event_with_keyboard(callback_query.from_user.id, int(temp[temp.find('#')+1:len(temp)]), all_events, 1)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


#@dp.callback_query_handler(lambda c: c.data[0:c.data.find('#')] == 'five')
async def process_callback_pagination_five(callback_query: types.CallbackQuery):
    all_events = await base.get_events()
    temp = callback_query.data
    await send_event_with_keyboard(callback_query.from_user.id, int(temp[temp.find('#')+1:len(temp)]), all_events, 5)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


#@dp.callback_query_handler(lambda c: c.data[0:c.data.find('#')] == 'confirmdelete')
async def process_confirmed_delete_event(callback_query: types.CallbackQuery):
    all_events = await base.get_events()
    temp = callback_query.data
    idx = int(temp[temp.find('#')+1:len(temp)])
    await base.del_event(all_events[idx])
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.reply_to_message.message_id)


#@dp.callback_query_handler(lambda c: c.data[0:c.data.find('#')] == 'canceldelete')
async def process_canceled_delete_event(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


def register_handlers_client(dp: Dispatcher, link_bot: Bot):
    global bot
    bot = link_bot
    dp.register_message_handler(process_get_catalogue, lambda message: message.text == 'Каталог', state=None)
    dp.register_callback_query_handler(process_callback_delete_event, lambda c: c.data[0:c.data.find('#')] == 'delete')
    dp.register_callback_query_handler(process_callback_pagination_one, lambda c: c.data[0:c.data.find('#')] == 'one')
    dp.register_callback_query_handler(process_callback_pagination_five, lambda c: c.data[0:c.data.find('#')] == 'five')
    dp.register_callback_query_handler(process_confirmed_delete_event, lambda c: c.data[0:c.data.find('#')] == 'confirmdelete')
    dp.register_callback_query_handler(process_canceled_delete_event, lambda c: c.data[0:c.data.find('#')] == 'canceldelete')


async def send_event_with_keyboard(user_id, idx, all_events, counter):
    while idx < len(all_events) and counter > 0:
        await send_event(user_id, idx, all_events)
        idx = idx + 1
        counter = counter - 1
    pagination_keyboard = InlineKeyboardMarkup()
    button_plus_one = InlineKeyboardButton('+1', callback_data=f'one#{idx}')
    button_plus_five = InlineKeyboardButton('+5', callback_data=f'five#{idx}')
    pagination_keyboard.add(button_plus_one, button_plus_five)
    await bot.send_message(user_id, 'Показать больше', reply_markup=pagination_keyboard)


async def send_event(user_id, idx, all_events):
    delete_event_keyboard = InlineKeyboardMarkup()
    if int(all_events[idx].author_id) == int(user_id):
        button_delete_event = InlineKeyboardButton('❌ Удалить событие', callback_data=f'delete#{idx}')
        delete_event_keyboard.add(button_delete_event)
    else:    
        button_contact_event = InlineKeyboardButton('Связаться', callback_data=f'contact#{idx}')
        delete_event_keyboard.add(button_contact_event)

    event_type = all_events[idx].event_media.split('#')[0]
    event_media = all_events[idx].event_media.split('#')[1]
    if event_type == 'photo':
        await bot.send_photo(user_id, event_media, caption=f'{all_events[idx].event_header}\n{all_events[idx].event_description}', reply_markup=delete_event_keyboard)
    if event_type == 'video':
        await bot.send_video(user_id, event_media, caption=f'{all_events[idx].event_header}\n{all_events[idx].event_description}', reply_markup=delete_event_keyboard)
    if event_type == 'audio':    
        await bot.send_audio(user_id, event_media, caption=f'{all_events[idx].event_header}\n{all_events[idx].event_description}', reply_markup=delete_event_keyboard)
    if event_type == 'animation':
        await bot.send_animation(user_id, event_media, caption=f'{all_events[idx].event_header}\n{all_events[idx].event_description}', reply_markup=delete_event_keyboard)

