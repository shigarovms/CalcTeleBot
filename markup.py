from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('Главное меню')


# MAIN MENU
btnRandom = KeyboardButton('Рандомное число')
btnOther = KeyboardButton('Другое')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRandom, btnOther)


# OTHER MENU
btnInfo = KeyboardButton('Информация')
btnMoney = KeyboardButton('Курсы')
otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnInfo, btnMoney, btnMain)