# Telegram bot, that calculates

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
# import markup as nav
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
    await message.answer('Привет!✋ Я бот-калькулятор. Посчитаю для тебя выражения типа ((34/2-15)**3 или 16*19-177',
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
                         '\n\nПример: ((34/2-15)**3',
                         reply_markup=inline_nav.calcKeyboard)
    await bot.send_message(message.from_user.id, 'Готов считать!')


# Обработчик сообщения из текстового поля
@dp.message_handler()
async def response_message(message: types.Message):
    try:
        x = eval(message.text)
        if x - int(x) == 0:
            answer = int(x)
        else:
            answer = x
    except ZeroDivisionError:
        answer = 'делить на ноль нельзя! не я это придумал 😁'
    except Exception:
        answer = 'Я умею считать арифметические выражения такие как (34/2-15)**3 или 33%3-7//4'
    else:
        answer = f'Готово! Посчитал! Вычислил! Вот, что у меня вышло: {message.text}={answer}'
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
                                        text=f'Ума не приложу, как такое посчитать:\n\n{exp_text[call.from_user.id]}',
                                        show_alert=True)
        answer = 'Готов считать!'
    else:
        answer = f'{exp_text[call.from_user.id]}={answer}'

    await bot.edit_message_text(text=answer, message_id=(call.message.message_id + 1),
                                chat_id=call.from_user.id)
    # Обнуляем строку ввода
    exp_text[call.from_user.id] = ''


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands)