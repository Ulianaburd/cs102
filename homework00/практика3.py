import typing as tp
import math

"""
Напишите программу, реализующую инженерный калькулятор. 
Предусмотрите следующие операции:
- Сложение
- Вычитание
- Деление
- Умножение
- Возведение в произвольную степень
- Возведение в квадрат
- Синус
- Косинус
- Тангенс
- Натуральный логарифм
- Десятичный логарифм
- Возможность ввода всей цепочки операций целиком и ее решение, 
если она введена корректно. Цепочка может содержать скобки (ДЛЯ ТЕХ, У КОГО ПОЛУЧИЛИСЬ 
ВСЕ ОСТАЛЬНЫЕ ЧАСТИ ЗАДАНИЯ)
- Перевод целого неотрицательного числа из десятичной системы счиления 
в произвольную

Для реализации тригонометрических функций можно использовать 
функции модуля math.
Продемонстрируйте работу программы. Для этого реализуйте соответствующее меню.

Примечание: при вводе значений для обработки предусмотрите, 
что пользователь может ввести не число или знак операции,
а что-то некорректное, и тогда вам нужно сообщать ему об этом 
и запрашивать новый ввод. 
Другими словами, в отдельной функции (или функциях) должна быть реализована 
проверка на ввод.
"""


def calc(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:

    if command == "+":
         return num_1 + num_2
    if command == "-":
        return num_1 - num_2
    if command == "/":
        if num_2 == 0:
            return "На ноль делить нельзя, введите другое число"
        else:
            return num_1 / num_2
    if command == "*":
        return num_1 * num_2
    if command == "**":
        return num_1 ** num_2
    if command == "sin":
        return math.sin(num_1)
    if command == "cos":
        return math.cos(num_1)
    if command == "tan":
        return math.tan(num_1)
    if command == "log10":
        return math.log10(num_1)
    else:
        return f"Неизвестный оператор: {command!r}."


def match_case_calc(command: str, num_1: float, num_2: float = 0) -> tp.Union[float, str]:
    match command:
        case "+":
            return num_1 + num_2
        case "-":
            return num_1 - num_2
        case "/":
            if num_2 == 0:
                return "На ноль делить нельзя, введите другое число"
            else:
                return num_1 / num_2
        case "*":
            return num_1 * num_2
        case "**":
            return num_1 ** num_2
        case "sin":
            return math.sin(num_1)
        case "cos":
            return math.cos(num_1)
        case "tan":
            return math.tan(num_1)
        case "log10":
            return math.log10(num_1)
        case _:
            return f"Неизвестный оператор: {command!r}."


def checked_input():
    while True:
        num = input("Enter number > ")
        n = num.split(".")
        if len(n) == 2 and n[0].isdigit() and n[1].isdigit() or num.isdigit():
            return float(num)


def num_of_inputs(operator):
    if operator in ("+", "-", "/", "*", "**"):
        num1 = checked_input()
        num2 = checked_input()
        return match_case_calc(operator, num1, num2)
    else:
        num = checked_input()
        return match_case_calc(operator, num)






if __name__ == "__main__":
    while True:
        COMMAND = input("Введите оперцию > ")
        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        print(num_of_inputs(COMMAND))