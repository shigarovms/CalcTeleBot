from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btnMain = InlineKeyboardButton(text='Главное меню', url='https://core.telegram.org/bots/api#callbackquery')


# MAIN MENU
btnRandom = InlineKeyboardButton(text='Рандомное число', url='https://core.telegram.org/bots/api#callbackquery')
btnOther = InlineKeyboardButton(text='Другое', url='https://core.telegram.org/bots/api#callbackquery')
mainMenu = InlineKeyboardMarkup(row_width=1).add(btnRandom, btnOther)


# OTHER MENU
btnInfo = InlineKeyboardButton(text='Информация', url='https://core.telegram.org/bots/api#callbackquery')
btnMoney = InlineKeyboardButton(text='Курсы', url='https://core.telegram.org/bots/api#callbackquery')
otherMenu = InlineKeyboardMarkup(row_width=1).add(btnInfo, btnMoney, btnMain)