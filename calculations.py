

from re import match


def exp_calculator(text):
    # Заменим 'x', который выдает гугл на 'умножить' на '*'
    expression = text.lower().replace('x', '*')

    # Проверим, подходит ли строка типа "5% от 69"
    if match(r'\d+%\W\w+\W\d+', text):
        procent = text.split('%')[0]
        tzeloe = text.split(' ')[-1]
        # Подготовим строку для вычисления процента
        expression = f'0.01*{procent}*{tzeloe}'
        result = eval(expression)
        answer = f'------------------>  {text} = {result}  <---------------------'
        return answer

    try:
        x = eval(expression)
        if x - int(x) == 0:
            x = int(x)
    except ZeroDivisionError:
        answer = 'делить на ноль нельзя! не я это придумал 😁'
    except Exception:
        answer = f'{text} ...хммм\nЯ умею считать арифметические выражения такие как (34/2-15)**3 или 33%3-7//4'
    else:
        answer = f'Готово! Посчитал! Вычислил! Вот, что у меня вышло: {expression}={x}'

    return answer


# print(exp_calculator('5% от 69'))
# print(exp_calculator('9 / 10'))
# print(sympify('9/10'))