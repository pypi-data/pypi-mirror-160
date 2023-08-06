from enum import IntEnum


class OperatorWeight(IntEnum):
    BRACKET_WEIGHT = 4
    EXPONENT_WEIGHT = 3
    DIVISION_MULTIPLICATION_WEIGHT = 2
    ADDITION_SUBTRACTION_WEIGHT = 1


def is_operator(value: str) -> bool:
    return value in ["+", "-", "*", "/", "(", ")", "^"]


def get_weight(operator: str) -> int:
    if not is_operator(operator):
        raise ValueError(f"{operator} is not an operator")

    weights = {
        "(": OperatorWeight.BRACKET_WEIGHT.value,
        ")": OperatorWeight.BRACKET_WEIGHT.value,
        "^": OperatorWeight.EXPONENT_WEIGHT.value,
        "/": OperatorWeight.DIVISION_MULTIPLICATION_WEIGHT.value,
        "*": OperatorWeight.DIVISION_MULTIPLICATION_WEIGHT.value,
        "+": OperatorWeight.ADDITION_SUBTRACTION_WEIGHT.value,
        "-": OperatorWeight.ADDITION_SUBTRACTION_WEIGHT.value,
    }

    return weights[operator]
