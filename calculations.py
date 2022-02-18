
# import re
from re import match


def text_prepared(text):
    expression = text.lower()
    expression = expression.replace(' х ', '*')
    expression = expression.replace(' x ', '*')
    expression = expression.replace(',', '.')
    expression = expression.replace('минус', '-')

    expression = expression.replace(' процентов', '%')
    expression = expression.replace(' процента', '%')
    expression = expression.replace(' процент', '%')
    expression = expression.replace('в степени', '**')
    expression = expression.replace('степени', '**')
    # print(expression)
    return expression


def procent_calc(exp):
    procent = float(exp.split('%')[0])
    tzeloe = float(exp.split(' ')[-1])
    x = (0.01 * procent * tzeloe)
    x = int(x) if x - int(x) == 0 else x
    return x


def exp_calculator(text):
    expression = text_prepared(text)

    # Проверим, подходит ли строка типа "5% от 69"
    if match(r'\d*.*\d+%\W\w+\W\d+', expression):
        answer = f'{text} = {procent_calc(expression)}'
        return answer
    try:
        x = eval(expression)
        x = int(x) if x - int(x) == 0 else x
    except ZeroDivisionError:
        answer = 'делить на ноль нельзя! не я это придумал 😁'
    except Exception:
        answer = f'{expression} ...хммм\nЯ умею считать арифметические выражения такие как (34/2-15)**3 или 33%3-7//4'
    else:
        answer = f'Готово! Вот, что у меня вышло: {expression} = {x}'

    return answer

