# Telegram bot, that calculates

from converter import text_from_ogg

import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils import executor, exceptions
from aiogram.types import ContentType, Message, InputFile
from asyncio import sleep
from os import remove

from StatesMachine import Support
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from calculations import exp_calculator
from InlineMarkup import calcKeyboard
import message_texts


# TODO сделать английскую версию бота
bot = Bot(token=os.environ['TOKEN'])
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
ADMIN_ID = '83418880'

# TODO make ExpressionTexts Database
exp_text = {}
got_answers = {}


# Список команд
async def setup_bot_commands(dp):
    bot_commands = [
        types.BotCommand(command="/start", description="С чистого листа"),
        types.BotCommand(command="/keys", description="Вызов клавиатуры"),
        types.BotCommand(command="/help", description="Нужна помощь?"),
        types.BotCommand(command="/support", description="Отзывы и предложения"),
        types.BotCommand(command="/arithmetics", description="Знаки и правила")
    ]
    await bot.set_my_commands(bot_commands)


# TODO добавить возможность оставлять отзывы и предложения
# /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # На старте в словаре создаем пустую строку для записи выражения каждого пользователя
    current_user_id = message.from_user.id

    got_answers[current_user_id] = ''
    # Приветствуем
    await message.answer(text= message_texts.hello_on_start, reply_markup=calcKeyboard)
    await bot.send_message(message.from_user.id, 'Готов считать!')
    await setup_bot_commands(dp)


# /keys
@dp.message_handler(commands=['keys'])
async def process_keys_command(message: types.Message):
    await message.answer(text=message_texts.keys_text, reply_markup=calcKeyboard, parse_mode=types.ParseMode.MARKDOWN)
    await bot.send_message(message.from_user.id, 'Готов считать!')


# /arithmetics
@dp.message_handler(commands=['arithmetics'])
async def process_help_command(message: types.Message):
    await message.answer(text=message_texts.arithmetics_help_text, parse_mode=types.ParseMode.MARKDOWN)


# /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer(text=message_texts.help_text)


# # /support
# @dp.message_handler(commands=['support'])
# async def process_help_command(message: types.Message):
#     await message.answer(text=message_texts.help_text)


# ------------------------------------------------------------------------HANDLERS--------------------------------------
# Защита от quit()
@dp.message_handler(regexp=r'\w+\(\)\w*')
async def quit_protection(message: types.Message):
    await bot.send_message(message.from_user.id, text= message_texts.no_hack_text, reply_markup=calcKeyboard)
    await bot.send_message(message.from_user.id, 'Готов считать!')


# Переход в состояние Support.ContactSupport по команде /support
@dp.message_handler(Command('support'), state=None)
async def talk_to_support(message: types.Message):
    await message.answer(message_texts.support_is_on)
    await Support.ContactSupport.set()


@dp.message_handler(state=Support.ContactSupport)
# TODO В этот хендлер не попадают аудиосообщения и картинки даже в state=Support.ContactSupport. А должны
async def forward_to_support(message, state: FSMContext):
    print('user_voice here')
    if message.text != '/support':
        await message.forward(chat_id=ADMIN_ID)
    await state.finish()
    await message.answer(message_texts.support_is_off)


# Обработчик сообщения из текстового поля
@dp.message_handler(state=None)
async def response_message(message: types.Message):
    user_id = message.from_user.id
    answer_text, exp_text[user_id] = exp_calculator(message.text)
    if 'Готово!' in answer_text:
        await bot.send_message(message.from_user.id, answer_text, parse_mode=types.ParseMode.MARKDOWN)
    else:
        await bot.send_message(message.from_user.id, answer_text, reply_markup=calcKeyboard)
        await bot.send_message(message.from_user.id, 'Готов считать!')


# 1 input callback - добавляем символ к выражению в строке ввода
@dp.callback_query_handler(text_contains='input')
async def expression_constructor_keys(call: types.callback_query):
    user_id = call.from_user.id
    # Если записи с выражением пользователя не существует, запишем пустую строку
    exp_text[user_id] = exp_text[user_id] if user_id in exp_text else ''

    edit_msg_id = call.message.message_id + 1
    symb_to_add = call.data[-1]

    if len(exp_text[user_id]) > 1 and exp_text[user_id][0] == ' ':
            if symb_to_add in '+-x/':
                exp_text[user_id] = exp_text[user_id][1:] + symb_to_add
            else:
                exp_text[user_id] = symb_to_add
    else:
        exp_text[user_id] += symb_to_add

    await bot.edit_message_text(text=exp_text[user_id], message_id=edit_msg_id, chat_id=user_id)


# 2 delete callback - удаляем последний символ выражения
@dp.callback_query_handler(text_contains='delete')
async def delete_from_expression(call: types.callback_query):
    exp_text[call.from_user.id] = exp_text[call.from_user.id][:-1]
    try:
        await bot.edit_message_text(text=exp_text[call.from_user.id],
                                    message_id=(call.message.message_id + 1),
                                    chat_id=call.from_user.id)
    except exceptions.MessageTextIsEmpty:
        try:
            await bot.edit_message_text(text='Готов считать!',
                                        message_id=(call.message.message_id + 1),
                                        chat_id=call.from_user.id)
        except exceptions.MessageNotModified:
            pass


# 3 calculate callback - вычисляем выражение
@dp.callback_query_handler(text_contains='calculate')
async def expression_calculate(call: types.callback_query):
    user_id = call.from_user.id
    # Изменяем сообщение, следующее за тем, ка которому прикреплена клавиатура
    edit_msg_id = call.message.message_id + 1

    if exp_text[user_id] == '' or exp_text[user_id] == 'quit()':
        return
    else:
        try:
            x = eval(exp_text[user_id].replace('х', '*').replace('x', '*'))
            answer = int(x) if x - int(x) == 0 else x
        except ZeroDivisionError:
            answer_text = message_texts.zero_division_text
        except Exception:
            # PopUp уведомление
            popup_text = f'Ума не приложу, как такое посчитать:\n\n{exp_text[user_id]}\n🙄'
            await bot.answer_callback_query(callback_query_id=call.id, text=popup_text, show_alert=True)

            # Делаем, чтобы на непонятое выражение 10 секунд смотрел снизу смайлик, а потом исчезал
            answer_text = f'{exp_text[user_id]}\n🙄'
            await bot.edit_message_text(text=answer_text, message_id=edit_msg_id, chat_id=user_id)
            await sleep(7)
            await bot.edit_message_text(text=exp_text[user_id], message_id=edit_msg_id, chat_id=user_id)
            return
        else:
            # *bold* _italic_ `fixed width font` [link](http://google.com).
            answer_text = f'`{answer}` = {exp_text[user_id]}'
            # Обнуляем строку ввода
            exp_text[user_id] = f' {answer}'
    await bot.edit_message_text(text=answer_text, message_id=edit_msg_id,
                                chat_id=user_id, parse_mode=types.ParseMode.MARKDOWN)


# Обработчик голосового сообщения
@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: Message):
    user_id = message.from_user.id
    # Если записи с выражением пользователя не существует, запишем пустую строку
    exp_text[user_id] = exp_text[user_id] if user_id in exp_text else ''

    # TODO сделать возможным продолжение расчетов голосом. Например в предыдущий раз ответ был 69,
    #  дальше пользователь шлет сообщение 'ответ' умножить на 54-7 -> *(54-7)
    # File management голосового сообщения:
    voice = await message.voice.get_file()
    ogg_file = f'{voice.file_id}.ogg'
    await bot.download_file(file_path=voice.file_path, destination=ogg_file)

    text_from_speech = text_from_ogg(ogg_file)

    # Если начали фразу со слова ответ, подставить результат предыдущего вычисления вместо слова ответ
    if text_from_speech.split(' ')[0] == 'ответ':
        if len(exp_text[user_id]) > 1:
            if exp_text[user_id][0] == ' ':
                exp_text[user_id] = text_from_speech.replace('ответ', exp_text[user_id][1:])
    else:
        exp_text[user_id] = text_from_speech

    remove(ogg_file)

    answer_text, exp_text[user_id] = exp_calculator(exp_text[user_id])

    if 'Готово!' in answer_text:
        await bot.send_message(user_id, answer_text, parse_mode=types.ParseMode.MARKDOWN)
    else:
        await bot.send_message(user_id, answer_text,  reply_markup=calcKeyboard)
        await bot.send_message(user_id, 'Готов считать!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup= setup_bot_commands)
