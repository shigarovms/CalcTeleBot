from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
#import markup as nav
import InlineMarkup as inline_nav

bot = Bot(token='1110437563:AAHRe3H8X5MUSstLnqy0c1fSyIyCNIBxxmc')
dp = Dispatcher(bot)
exp_text = {}

# Список команд бота
async def setup_bot_commands(dp):
    bot_commands = [
        types.BotCommand(command="/help", description="Get info about me")
    ]
    await bot.set_my_commands(bot_commands)

# Обработка команд
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    current_user_id = message.from_user.id
    exp_text[current_user_id] = ''
    await message.answer('Привет!\nЯ калькулятор. Посчитаю для тебя выражения типа\n\n((34/2-15)**3', reply_markup=inline_nav.mainMenu)

@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await message.answer('Не знаю, как тебе помочь, чувак...?\nНачни ввод, например', reply_markup=inline_nav.mainMenu)


@dp.message_handler()
async def response_message(message: types.Message):
    try:
        x = eval(message.text)
    except ZeroDivisionError:
        answer = 'делить на ноль нельзя! не я это придумал 😁'
    except Exception:
        answer = 'Я умею считать только арифметические выражения типа: \n(34/2-15)**3'
    else:
        answer = f'Вот, что у меня вышло:\n{message.text}={x}'
    await bot.send_message(message.from_user.id, answer, reply_markup=inline_nav.mainMenu)


@dp.callback_query_handler(text='Калькулятор')
async def showCalc(message: types.Message):
    
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Вводите _____________________', reply_markup=inline_nav.calcKeyboard)


# async def input_to_expression(call: types.callback_query):
#     print('начинаем запись')
#     exp_text = ''
#     while True:
#         print('вошли в while')
#
#         @dp.callback_query_handler(text_contains='input')
#         async def add_to_expression(call: types.callback_query):
#             print('вошли в add_to_expression')
#             symbToAdd = call.data[-1]
#             #global exp_text
#             input_to_expression.exp_text += symbToAdd
#             await bot.delete_message(call.from_user.id, call.message.message_id)
#             await bot.send_message(call.from_user.id, text=input_to_expression.exp_text+' _____________________________'[:-len(input_to_expression.exp_text)], reply_markup=inline_nav.calcKeyboard)
#
#
#     else:
#         return exp_text


# async def expression_calculate(exp_text):
#     try:
#         x = eval(exp_text)
#     except ZeroDivisionError:
#         return 'делить на ноль нельзя! не я это придумал 😁'
#     except Exception:
#         return 'Я умею считать только арифметические выражения типа: \n(34/2-15)**3\nПопробуйте:'
#     else:
#         return f'{exp_text}={x}'


# @dp.callback_query_handler(text_contains='input')
# async def expression_consrtuctor(call: types.callback_query):
#     exp_text = await input_to_expression(call)
#     answer = await expression_calculate(exp_text)
#     await bot.send_message(call.from_user.id, answer + ' ____________________________'[:-len(answer)],
#                            reply_markup=inline_nav.calcKeyboard)


@dp.callback_query_handler(text_contains='input')
async def expression_consrtuctor(call: types.callback_query):
    symbToAdd = call.data[-1]
    #global exp_text
    exp_text[call.from_user.id] += symbToAdd
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, text=exp_text[call.from_user.id]+' _____________________________'[:-len(exp_text)], reply_markup=inline_nav.calcKeyboard)


@dp.callback_query_handler(text_contains='delete')
async def delete_from_expression(call: types.callback_query):
    #global exp_text
    exp_text[call.from_user.id] = exp_text[call.from_user.id][:-1]
    await bot.delete_message(call.from_user.id, call.message.message_id)
    try:
        await bot.send_message(call.from_user.id, text=exp_text[call.from_user.id], reply_markup=inline_nav.calcKeyboard)
    except exceptions.MessageTextIsEmpty:
        await bot.send_message(call.from_user.id, text='Вводите _____________________', reply_markup=inline_nav.calcKeyboard)


@dp.callback_query_handler(text_contains='calculate')
async def expression_calculate(call: types.callback_query):

    try:
        x = eval(exp_text[call.from_user.id])
    except ZeroDivisionError:
        answer = 'делить на ноль нельзя! не я это придумал 😁'
    except Exception:
        answer = 'Я умею считать только арифметические выражения типа: \n(34/2-15)**3\nПопробуйте:'
    else:
        answer = f'{exp_text[call.from_user.id]}={x}'
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, answer+' ____________________________'[:-len(answer)], reply_markup=inline_nav.calcKeyboard)
    exp_text[call.from_user.id] = ''


# @dp.callback_query_handler(text='Другое')
# async def mainMenu_show(message: types.Message):
#     await bot.delete_message(message.from_user.id, message.message.message_id)
#     await bot.send_message(message.from_user.id, 'Посмотрим, что еще у нас есть...', reply_markup=inline_nav.otherMenu)
#
#
# @dp.callback_query_handler(text='Главное меню')
# async def mainMenu_show(message: types.Message):
#     await bot.delete_message(message.from_user.id, message.message.message_id)
#     await bot.send_message(message.from_user.id, 'Главное меню:', reply_markup=inline_nav.mainMenu)
#
#
# @dp.callback_query_handler(text='Удалить')
# async def mainMenu_show(message: types.Message):
#     await bot.delete_message(message.from_user.id, message.message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands)