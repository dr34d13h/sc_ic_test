from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, types, Dispatcher
from aiogram.utils.emoji import emojize
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboard import cancel_operation_keyboard, welcome_keyboard
import base


bot = None


class FSMAdmin(StatesGroup):
    event_name = State()
    event_header = State()
    event_description = State()
    event_media = State()
    event_date = State()


#@dp.message_handler(lambda messasge: message.text == '❌Отменить операцию')
async def process_cancel_operation(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, 'Вы отменили операцию', reply_markup=welcome_keyboard)


#@dp.message_handler(lambda message: message.text == 'Добавить событие', state=None)
async def process_create_event(message: types.Message):
    await FSMAdmin.event_name.set()
    await bot.send_message(message.from_user.id, 'Вы создаёте событие', reply_markup=cancel_operation_keyboard)
    await message.reply('Введите имя события')


#@dp.message_handler(state=FSMAdmin.event_name)
async def process_get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_name'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите заголовок события')


#@dp.message_handler(state=FSMAdmin.event_header)
async def process_get_header(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_header'] = message.text
    await FSMAdmin.next()
    await message.reply('Введите описание события')


#@dp.message_handler(state=FSMAdmin.event_description)
async def process_get_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_description'] = message.text
    await FSMAdmin.next()
    await message.reply('Загрузите фото')


#@dp.message_handler(content_types=['photo', 'video', 'audio', 'animation'], state=FSMAdmin.event_media)
async def process_get_media(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.photo:
            data['event_media'] = ('photo', message.photo[0].file_id)
        if message.video:
            data['event_media'] = ('video', message.video.file_id)
        if message.audio:
            data['event_media'] = ('audio', message.audio.file_id)
        if message.animation:
            data['event_media'] = ('animation', message.animation.file_id)
    await FSMAdmin.next()
    empty_keyboard = InlineKeyboardMarkup()
    button_empty = InlineKeyboardButton('Оставить пустым', callback_data=f'empty')
    empty_keyboard.add(button_empty)
    await message.reply('Введите дату', reply_markup=empty_keyboard)


#@dp.message_handler(state=FSMAdmin.event_date)
async def process_get_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_date'] = message.text
        caption_text = 'Имя события: ' + str(data['event_name']) + '\n' + 'Заголовок: ' + str(data['event_header']) + '\n' + 'Описание: ' + str(data['event_description']) + '\n' + 'Дата: ' + str(data['event_date']) + '\n'
        event_type = data['event_media'][0]
        event_media = data['event_media'][1]
        if event_type == 'photo':
            bot.send_photo(message.from_user.id, event_media, caption=caption_text)
        if event_type == 'video':
            bot.send_video(message.from_user.id, event_media, caption=caption_text)
        if event_type == 'audio':
            bot.send_audio(message.from_user.id, event_media, caption=caption_text)
        if event_type == 'animation':
            bot.send_animation(message.from_user.id, event_media, caption=caption_text)
        await base.add_event(data, message.from_user.id)
    await bot.send_message(message.from_user.id, emojize('Вы создали событие. :point_up_2::point_up_2::point_up_2:'), reply_markup=welcome_keyboard)
    await state.finish()

#@dp.callback_query_handler(lambda c: c.data == 'empty', state=FSMAdmin.event_date)
async def process_get_empty_date_event(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['event_date'] = ' '
        caption = 'Имя события: ' + str(data['event_name']) + '\n' + 'Заголовок: ' + str(data['event_header']) + '\n' + 'Описание: ' + str(data['event_description']) + '\n'
        event_type = data['event_media'][0]
        event_media = data['event_media'][1]
        if event_type == 'photo':
            bot.send_photo(message.from_user.id, event_media, caption=caption_text)
        if event_type == 'video':
            bot.send_video(message.from_user.id, event_media, caption=caption_text)
        if event_type == 'audio':
            bot.send_audio(message.from_user.id, event_media, caption=caption_text)
        if event_type == 'animation':
            bot.send_animation(message.from_user.id, event_media, caption=caption_text)
        await base.add_event(data, callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id, emojize('Вы создали событие. :point_up_2::point_up_2::point_up_2:'), reply_markup=welcome_keyboard)
    await state.finish()


def register_handlers_client(dp: Dispatcher, link_bot: Bot):
    global bot
    bot = link_bot
    dp.register_callback_query_handler(process_get_empty_date_event, lambda c: c.data == 'empty', state=FSMAdmin.event_date)
    dp.register_message_handler(process_cancel_operation, lambda message: message.text == '❌Отменить операцию', state=FSMAdmin.event_name)
    dp.register_message_handler(process_cancel_operation, lambda message: message.text == '❌Отменить операцию', state=FSMAdmin.event_header)
    dp.register_message_handler(process_cancel_operation, lambda message: message.text == '❌Отменить операцию', state=FSMAdmin.event_description)
    dp.register_message_handler(process_cancel_operation, lambda message: message.text == '❌Отменить операцию', state=FSMAdmin.event_media)
    dp.register_message_handler(process_cancel_operation, lambda message: message.text == '❌Отменить операцию', state=FSMAdmin.event_date)
    dp.register_message_handler(process_create_event, lambda message: message.text == 'Добавить событие', state=None)
    dp.register_message_handler(process_get_name, state=FSMAdmin.event_name)
    dp.register_message_handler(process_get_header, state=FSMAdmin.event_header)
    dp.register_message_handler(process_get_description, state=FSMAdmin.event_description)
    dp.register_message_handler(process_get_media, content_types=['photo', 'video', 'audio', 'animation'], state=FSMAdmin.event_media)
    dp.register_message_handler(process_get_date, state=FSMAdmin.event_date)

