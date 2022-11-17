#  PUT YOUR CODE HERE
import math
import typing as tp


def calc(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:
    if command == "+":
        return num_1 + num_2
    if command == "-":
        return num_1 - num_2
    if command == "/" or ":":
        if num_2 == 0:
            return "На ноль делить нельзя, введите другое число"
        return num_1 / num_2
    if command == "*":
        return num_1 * num_2
    if command == "**":
        return num_1**num_2
    if command == "sin":
        return math.sin(num_1)
    if command == "cos":
        return math.cos(num_1)
    if command == "tan":
        return math.tan(num_1)
    if command == "log10":
        return math.log10(num_1)
    if command == "log1p":
        return math.log1p(num_1)
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
        case ":":
            if num_2 == 0:
                return "На ноль делить нельзя, введите другое число"
            else:
                return num_1 / num_2
        case "*":
            return num_1 * num_2
        case "**":
            return num_1**num_2
        case "sin":
            return math.sin(num_1)
        case "cos":
            return math.cos(num_1)
        case "tan":
            return math.tan(num_1)
        case "log10":
            return math.log10(num_1)
        case "log1p":
            return math.log1p(num_1)
        case _:
            return f"Неизвестный оператор: {command!r}."


def checked_input():
    num = input("Enter number > ")
    try:
        return float(num)
    except ValueError:
        return checked_input()


def num_of_inputs(operator):
    if operator in ("+", "-", "/", ":", "*", "**"):
        num1 = float(checked_input())
        num2 = float(checked_input())
        return match_case_calc(operator, num1, num2)
    else:
        num = checked_input()
        return match_case_calc(operator, num)


def is_float(num: tp.Any) -> bool:
    """Проверка, что число вещественное"""
    try:
        float(num)
    except ValueError:
        return False
    return True


def brackets_are_ok(string_eq):
    """Проверка, корректно ли стоят скобки в выражении"""
    brackets = 0
    for char in string_eq:
        if char == "(":
            brackets += 1
        elif char == ")":
            brackets -= 1
            if brackets < 0:
                ok = False
                break
    else:
        ok = not brackets
    return ok


priors = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3, "s": 4, "c": 4, "t": 4, "l": 4, "n": 4, "g": 4}


def get_string_eq(given: tp.Optional[str] = None) -> str:
    """Получение выражения со скобочками или без"""
    string_eq = input("Введите выражение > ") if given is None else given
    if brackets_are_ok(string_eq):
        string_eq = (
            string_eq.replace(" ", "")
            .replace("ctg", "g")
            .replace("sin", "s")
            .replace("cos", "c")
            .replace("tg", "t")
            .replace("log10", "l")
            .replace("ln", "n")
        )
        if string_eq.find("#") != -1:
            return "Операция перевода в другую СС не поддерживается для опции ввода выражения целиком."
        return string_eq
    return "Скобки стоят неправильно!"


def solve(string_eq: str) -> tp.Union[float, str]:
    """Решение полноценного выражения"""
    if string_eq == "":
        return ""
    if is_float(string_eq):
        return float(string_eq)
    else:
        in_brackets = 0
        best_opt = 5
        found_outside_brackets = -1
        for i, char in enumerate(string_eq):
            if char == "(":
                in_brackets += 1
            elif char == ")":
                in_brackets -= 1
            elif char in "+-*/^sctlng":
                if in_brackets == 0 and priors[char] <= best_opt:
                    found_outside_brackets = i
                    best_opt = priors[char]
        if found_outside_brackets == -1:
            if string_eq[0] == "(" and string_eq[-1] == ")":
                return solve(string_eq[1:-1])
            return string_eq
        else:
            inner_1 = solve(string_eq[:found_outside_brackets])
            inner_2 = solve(string_eq[found_outside_brackets + 1 :])
            op = string_eq[found_outside_brackets]

            if inner_1 == "" and is_float(inner_2):
                return match_case_calc(op, 0.0, float(inner_2)) if op == "-" else match_case_calc(op, float(inner_2))
            if is_float(inner_1) and is_float(inner_2):
                return match_case_calc(op, float(inner_1), float(inner_2))
            return inner_1 if inner_1 == " " else inner_2


if __name__ == "__main__":
    while True:
        COMMAND = input("Введите оперцию > ")

        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        print(num_of_inputs(COMMAND))
