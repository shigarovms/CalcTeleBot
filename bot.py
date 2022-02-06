from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token='1110437563:AAHRe3H8X5MUSstLnqy0c1fSyIyCNIBxxmc')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer("Привет!\nЯ калькулятор. Посчитаю для тебя выражения типа\n\n(2+1)*7/5-69")


@dp.message_handler()
async def response_message(message: types.Message):
    try:
        x = eval(message.text)
    except ZeroDivisionError:
        answer = 'делить на ноль нельзя! не я это придумал.'
    except Exception:
        answer = 'Я умею считать только арифметические выражения типа: \n(34+1)/5'
    except ZeroDivisionError:
        answer = 'делить на ноль нельзя! не я это придумал 😁'
    else:
        answer = f'Вот, что у меня вышло:\n{message.text}={x}'

    await bot.send_message(message.from_user.id, answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)