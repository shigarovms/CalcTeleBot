# Telegram bot, that calculates

from time import sleep
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from aiogram.types import ContentType, File, Message
from converter import text_from_ogg
from os import remove
from calculations import exp_calculator
import InlineMarkup as inline_nav


bot = Bot(token='1110437563:AAHRe3H8X5MUSstLnqy0c1fSyIyCNIBxxmc')
dp = Dispatcher(bot)
exp_text = {}


# Список команд
async def setup_bot_commands(dp):
    bot_commands = [
        types.BotCommand(command="/start", description="С чистого листа"),
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
                         reply_markup=inline_nav.calcKeyboard)

    await bot.send_message(message.from_user.id, 'Готов считать!')
    await setup_bot_commands(dp)

# /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.answer('Нажимай циферки, знаки, скобки! '
                         '\nПосле того как нажмешь = я посчитаю твое выражение, если оно арифметически верно. '
                         '\nТакже можешь ввести выражение в поле "Сообщение" внизу. '
                         'Отправляй его мне без знака = в конце - я посчитаю. '
                         '\n\nЕще я обрабатываю голосовые сообщения! 144-27 или 5% от 169 Попробуй! '
                         '\n\nПример: ((34/2-15)**3',
                         reply_markup=inline_nav.calcKeyboard)
    await bot.send_message(message.from_user.id, 'Готов считать!')


# Защита от quit()
@dp.message_handler(regexp=r'\w+\(\)\w*')
async def quit_protection(message: types.Message):
    await bot.send_message(message.from_user.id, 'Хорошая попытка, мистер хаккер! Но меня так лекго не выключить.',
                           reply_markup=inline_nav.calcKeyboard)
    await bot.send_message(message.from_user.id, 'Готов считать!')


# Обработчик сообщения из текстового поля
@dp.message_handler()
async def response_message(message: types.Message):
    answer = exp_calculator(message.text)
    # try:
    #     x = eval(message.text)
    #     if x - int(x) == 0:
    #         answer = int(x)
    #     else:
    #         answer = x
    # except ZeroDivisionError:
    #     answer = 'делить на ноль нельзя! не я это придумал 😁'
    # except Exception:
    #     answer = 'Я умею считать арифметические выражения такие как (34/2-15)**3 или 33%3-7//4'
    # else:
    #     answer = f'Готово! Посчитал! Вычислил! Вот, что у меня вышло: {message.text}={answer}'
    await bot.send_message(message.from_user.id, answer, reply_markup=inline_nav.calcKeyboard)
    await bot.send_message(message.from_user.id, 'Готов считать!')


# 1
# input callback - добавляем символ к выражению в строке ввода
@dp.callback_query_handler(text_contains='input')
async def expression_consrtuctor_keys(call: types.callback_query):
    symbToAdd = call.data[-1]
    exp_text[call.from_user.id] += symbToAdd
    await bot.edit_message_text(text=exp_text[call.from_user.id],
                                message_id=(call.message.message_id + 1),
                                chat_id=call.from_user.id)


# 2
# delete callback - удаляем последний символ выражения
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


# 3
# calculate callback - вычисляем выражение
@dp.callback_query_handler(text_contains='calculate')
async def expression_calculate(call: types.callback_query):
    if exp_text[call.from_user.id] == '' or exp_text[call.from_user.id] == 'quit()':
        return
    else:

        try:
            x = eval(exp_text[call.from_user.id])
            if x - int(x) == 0:
                answer = int(x)
            else:
                answer = x
        except ZeroDivisionError:
            answer = 'делить на ноль нельзя! не я это придумал 😁'
        except Exception:
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=f'Ума не приложу, как такое посчитать:'
                                                 f'\n\n{exp_text[call.from_user.id]}',
                                            show_alert=True)
            answer = f'{exp_text[call.from_user.id]}' \
                     f'\n🙄'
            await bot.edit_message_text(text=answer,
                                        message_id=(call.message.message_id + 1),
                                        chat_id=call.from_user.id)
            sleep(3)
            await bot.edit_message_text(text=exp_text[call.from_user.id],
                                        message_id=(call.message.message_id + 1),
                                        chat_id=call.from_user.id)
            return
        else:
            answer = f'{exp_text[call.from_user.id]}={answer}'
            # Обнуляем строку ввода
            exp_text[call.from_user.id] = ''

    await bot.edit_message_text(text=answer, message_id=(call.message.message_id + 1),
                                chat_id=call.from_user.id)


# @dp.message_handler(content_types=[ContentType.VOICE])
# async def voice_message_handler(message: Message):
#     voice = await message.voice.get_file()
#     await bot.download_file(file_path=voice.file_path, destination=f'{voice.file_id}.ogg')
#     expression = text_from_ogg(f'{voice.file_id}.ogg')
#     remove(f'{voice.file_id}.ogg')
#     answer = exp_calculator(expression)
#     await bot.send_message(message.from_user.id, answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands)