import pytest

from toolkit.calculator import Calc
from toolkit.errors import CalcError


def calc(expression: str):
    """Function to pass the expression through the core."""
    c = Calc()
    c.tokenization(expression)
    c.validation()
    return c.calculation()


# positive tests

def test_add():
    assert calc("2+3") == 5


def test_subtraction():
    assert calc("10-4") == 6


def test_multiplication():
    assert calc("3*4") == 12


def test_division():
    assert calc("10/4") == 2.5


def test_float_numbers():
    assert calc("2.5+1.5") == 4.0


def test_priority_1():
    assert calc("2+3*4") == 14


def test_priority_2():
    assert calc("10-6/2") == 7


def test_spaces_ignored():
    assert calc("2   +   3   *   4") == 14


def test_unary_minus():
    assert calc("-5+3") == -2


def test_unary_plus():
    assert calc("+5+3") == 8


def test_unary_minus_after_operator():
    assert calc("2*-3") == -6


def test_double_minus():
    assert calc("--5") == 5


def test_triple_minus():
    assert calc("---5") == -5


# negative tests

def test_empty_expression():
    c = Calc()
    with pytest.raises(CalcError):
        c.tokenization("")


def test_only_spaces():
    c = Calc()
    with pytest.raises(CalcError):
        c.tokenization("   ")


def test_unknown_symbol():
    c = Calc()
    with pytest.raises(CalcError):
        c.tokenization("2 $ 3")


def test_missing_operand_at_end():
    c = Calc()
    c.tokenization("2+")
    with pytest.raises(CalcError):
        c.validation()


def test_two_binary_operators():
    c = Calc()
    c.tokenization("2+*3")
    with pytest.raises(CalcError):
        c.validation()


def test_division_by_zero():
    c = Calc()
    c.tokenization("5/0")
    with pytest.raises(CalcError):
        c.validation()


def test_invalid_float_format():
    c = Calc()
    c.tokenization("2..5")
    with pytest.raises(CalcError):
        c.validation()
