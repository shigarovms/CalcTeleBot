
# import re
from re import match, split as resplit
from numpy import cbrt
from message_texts import zero_division_text


# TODO Решить проблему с млн
# TODO сделать возможным подсчет типа "корень степени 3 из 2 умножить на 6 + 5"

def text_prepared(text):
    expression = text.lower()

    if 'млн' in expression:
        spltd_exp = resplit(r'[+\-x/]', expression)
        for sub in spltd_exp:
            if 'млн' in sub:
                try:
                    new_sub = f'{int(sub.split("млн")[0]) * 1000000 + int(sub.split("млн")[1])} '
                except:
                    new_sub = f'{int(sub.split("млн")[0]) * 1000000} '
                    #     TODO ValueError: invalid literal for int() with base 10: 'кубический корень из 2 '
                expression = expression.replace(sub, new_sub)

    # expression = expression.replace(' х ', '*')        # Делаю это в eval()
    # expression = expression.replace(' x ', '*')
    # expression = expression.replace('.', '')          # мешает при использовании ответа с десятичной частью
    expression = expression.replace(',', '.')
    # expression = expression.replace(' млн ', '000000')
    expression = expression.replace('плюс', '+')
    expression = expression.replace('минус ', '-')
    expression = expression.replace('- ', '-')

    expression = expression.replace(' процентов', '%')
    expression = expression.replace(' процента', '%')
    expression = expression.replace(' процент', '%')
    expression = expression.replace('в степени', 'xx')
    expression = expression.replace('степени', 'xx')
    expression = expression.replace('^', 'xx')
    expression = expression.replace('корень xx', 'корень степени')

    expression = expression.replace('открытая скобка', '(')
    expression = expression.replace('закрытая скобка', ')')
    expression = expression.replace('открыть скобку', '(')
    expression = expression.replace('закрыть скобку', ')')
    # print(expression)
    return expression


def procent_calc(exp):
    procent = float(exp.split('%')[0])
    tzeloe = float(exp.split(' ')[-1])
    x = (0.01 * procent * tzeloe)
    x = int(x) if x - int(x) == 0 else x
    return x


def square_root_calc(exp):
    a = float(exp.split(' ')[-1])
    x = (a ** 2 ** -1)
    x = int(x) if x - int(x) == 0 else x
    return x


def cube_root_calc(exp):
    a = float(exp.split(' ')[-1])
    x = cbrt(a)
    try:
        x = int(x) if x - int(x) == 0 else x
    except:
        pass
    return x


def any_root_calc(exp):
    exp = exp.replace('корень степени', '')
    n = float(exp.split(' ')[1])
    a = float(exp.split(' ')[-1])
    x = pow(a, 1/n)
    try:
        x = int(x) if x - int(x) == 0 else x
    except:
        pass
    return x


def exp_calculator(text):
    expression = text_prepared(text)
    # print(expression)

    # Проверим, вычисление ли это процента
    if match(r'\d*.*\d+%\W\w+\W\d*.*\d+', expression):
        result = procent_calc(expression)
        answer_text = f'Готово! `{result}` = {text}'
        return answer_text, f' {result}'

    # Проверим, вычисление ли это квадратного корня
    if match(r'квадратный корень\W\w+\W-?\d*.*\d+', expression):
        result = square_root_calc(expression)
        answer_text = f'Готово! `{result}` = {text}'
        return answer_text, f' {result}'

    # Проверим, вычисление ли это кубического корня
    if match(r'кубический корень\W\w+\W-?\d*.*\d+', expression):
        result = cube_root_calc(expression)
        answer_text = f'Готово! `{result}` = {text}'
        return answer_text, f' {result}'

    # Проверим, вычисление ли это корня n-ой степени из a
    if match(r'корень степени -?\d*.*\d+\W\w+\W-?\d*.*\d+', expression):
        result = any_root_calc(expression)
        answer_text = f'Готово! `{result}` = {text}'
        return answer_text, f' {result}'

    try:
        result = eval(expression.replace('х', '*').replace('x', '*'))
        result = int(result) if result - int(result) == 0 else result
    except ZeroDivisionError:
        answer_text = zero_division_text
        result = ''
    except Exception:
        answer_text = f'{expression} ...хммм... 🤔\n' \
                      f'Я умею считать арифметические выражения, такие как (34/2-15)xx3 или 33//3-7/4'
        result = ''
    else:
        answer_text = f'Готово! Вот, что у меня вышло:\n`{result}` = {expression}'

    return answer_text, f' {result}'
