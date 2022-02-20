# Telegram bot, that calculates

import os
from boto.s3.connection import S3Connection
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from aiogram.types import ContentType, File, Message
from asyncio import sleep
from os import remove
from converter import text_from_ogg
from calculations import exp_calculator
from InlineMarkup import calcKeyboard
import VARS


# TODO Get token from Heroku config variables
# TOKEN = S3Connection(os.environ[''])
# print(type(TOKEN))
bot = Bot(token=os.environ('TOKEN'))
# bot = Bot(token=VARS.TOKEN)
dp = Dispatcher(bot)

# TODO make ExpressionTexts Database
exp_text = {}


# Список команд
async def setup_bot_commands(dp):
    bot_commands = [
        types.BotCommand(command="/start", description="С чистого листа. Вызвать кнопки"),
        types.BotCommand(command="/help", description="Нужна помощь?")
    ]
    await bot.set_my_commands(bot_commands)


# /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # На старте в словаре создаем пустую строку для записи выражения каждого пользователя
    current_user_id = message.from_user.id
    exp_text[current_user_id] = ''
    # Приветствуем
    await message.answer('Привет!✋ Я бот-калькулятор. Посчитаю для тебя выражения типа ((34/2-15)**3 или 16*19-177'
                         '\n\nЕще я обрабатываю голосовые сообщения! 144-27 или "5% от 169" Попробуй! ',
                         reply_markup=calcKeyboard)

    await bot.send_message(message.from_user.id, 'Готов считать!')
    await setup_bot_commands(dp)

# /help
# TODO добавить возможность оставлять отзывы и предложения
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer('Нажимай циферки, знаки, скобки! '
                         '\nПосле того как нажмешь = я посчитаю твое выражение, если оно арифметически верно. '
                         '\nТакже можешь ввести выражение в поле "Сообщение" внизу. '
                         'Отправляй его мне без знака = в конце - я посчитаю. '
                         '\n\nЕще я обрабатываю голосовые сообщения! 144-27*10 или 5% от 169 Попробуй! '
                         '\n\nПример: ((34/2-15)**3',
                         reply_markup=calcKeyboard)
    await bot.send_message(message.from_user.id, 'Готов считать!')


# Защита от quit()
@dp.message_handler(regexp=r'\w+\(\)\w*')
async def quit_protection(message: types.Message):
    await bot.send_message(message.from_user.id, 'Хорошая попытка, мистер хаккер! Но меня так лекго не выключить.',
                           reply_markup=calcKeyboard)
    await bot.send_message(message.from_user.id, 'Готов считать!')


# Обработчик сообщения из текстового поля
@dp.message_handler()
async def response_message(message: types.Message):
    answer = exp_calculator(message.text)
    if 'Готово!' in answer:
        await bot.send_message(message.from_user.id, answer)
    else:
        await bot.send_message(message.from_user.id, answer, reply_markup=calcKeyboard)
        await bot.send_message(message.from_user.id, 'Готов считать!')


# 1 input callback - добавляем символ к выражению в строке ввода
@dp.callback_query_handler(text_contains='input')
async def expression_consrtuctor_keys(call: types.callback_query):
    id = call.from_user.id
    symbToAdd = call.data[-1]
    if id in exp_text:
        exp_text[call.from_user.id] += symbToAdd
    else:
        exp_text[call.from_user.id] = symbToAdd
    await bot.edit_message_text(text=exp_text[call.from_user.id],
                                message_id=(call.message.message_id + 1),
                                chat_id=call.from_user.id)


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
    id = call.from_user.id

    if exp_text[id] == '' or exp_text[id] == 'quit()':
        return
    else:
        try:
            x = eval(exp_text[id])
            if x - int(x) == 0:
                answer = int(x)
            else:
                answer = x
        except ZeroDivisionError:
            answer = 'делить на ноль нельзя! не я это придумал 😁'
        except Exception:
            await bot.answer_callback_query(callback_query_id=call.id, text=f'Ума не приложу, как такое посчитать:'
                                                                            f'\n\n{exp_text[id]}', show_alert=True)
            answer = f'{exp_text[id]}' \
                     f'\n🙄'
            await bot.edit_message_text(text=answer, message_id=(call.message.message_id + 1), chat_id=id)
            await sleep(5)
            await bot.edit_message_text(text=exp_text[id], message_id=(call.message.message_id + 1), chat_id=id)
            return
        else:
            answer = f'{exp_text[id]} = {answer}'
            # Обнуляем строку ввода
            exp_text[id] = ''
    await bot.edit_message_text(text=answer, message_id=(call.message.message_id + 1), chat_id=id)


# Обработчик голосового сообщения
@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message_handler(message: Message):
    # TODO сделать возможным продолжение расчетов голосом. Например в предыдущий раз ответ был 69,
    #  дальше пользователь шлет сообщение ответ умножить на 54-7 -> *(54-7)
    voice = await message.voice.get_file()
    ogg_file_name = f'{voice.file_id}.ogg'
    await bot.download_file(file_path=voice.file_path, destination=ogg_file_name)
    expression = text_from_ogg(ogg_file_name)
    remove(ogg_file_name)
    answer = exp_calculator(expression)
    if 'Готово!' in answer:
        await bot.send_message(message.from_user.id, answer)
    else:
        await bot.send_message(message.from_user.id, answer,  reply_markup=calcKeyboard)
        await bot.send_message(message.from_user.id, 'Готов считать!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands)