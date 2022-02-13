from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btnMain = InlineKeyboardButton(text='Главное меню', callback_data='Главное меню')
btnDelete = InlineKeyboardButton(text='Удалить', callback_data='Удалить')


# MAIN MENU
btnGoToCalc = InlineKeyboardButton(text='Начать ввод', callback_data='Начать ввод')
mainMenu = InlineKeyboardMarkup(row_width=1).add(btnGoToCalc)


# CALC KEYBOARD
btn1 = InlineKeyboardButton(text='1', callback_data='input1')
btn2 = InlineKeyboardButton(text='2', callback_data='input2')
btn3 = InlineKeyboardButton(text='3', callback_data='input3')
btn4 = InlineKeyboardButton(text='4', callback_data='input4')
btn5 = InlineKeyboardButton(text='5', callback_data='input5')
btn6 = InlineKeyboardButton(text='6', callback_data='input6')
btn7 = InlineKeyboardButton(text='7', callback_data='input7')
btn8 = InlineKeyboardButton(text='8', callback_data='input8')
btn9 = InlineKeyboardButton(text='9', callback_data='input9')
btn0 = InlineKeyboardButton(text='0', callback_data='input0')

btnOpen_ = InlineKeyboardButton(text='(', callback_data='input(')
btnClose = InlineKeyboardButton(text=')', callback_data='input)')
btnEmpty = InlineKeyboardButton(text=' ', callback_data='none')
btnDelet = InlineKeyboardButton(text='C', callback_data='delete')
btnDiv__ = InlineKeyboardButton(text='/', callback_data='input/')
btnMinus = InlineKeyboardButton(text='-', callback_data='input-')
btnMult_ = InlineKeyboardButton(text='*', callback_data='input*')
btnPlus_ = InlineKeyboardButton(text='+', callback_data='input+')

btnDot = InlineKeyboardButton(text='.', callback_data='input.')
btnEqu = InlineKeyboardButton(text='=️', callback_data='calculate')

calcKeyboard = InlineKeyboardMarkup(row_width=4).add(btnOpen_, btnClose, btnEmpty, btnDelet,
                                                  btn7, btn8, btn9, btnDiv__,
                                                  btn4, btn5, btn6, btnMinus,
                                                  btn1, btn2, btn3, btnMult_,
                                                  btn0, btnDot, btnEqu, btnPlus_)