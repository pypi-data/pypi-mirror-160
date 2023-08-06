#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `infix_evaluator` package."""

import pytest
from mighty_bedmas_calculator.infix_evaluator import evaluate


def test_evaluate_addition():
    assert evaluate("2+2") == "4"
    assert evaluate("(2+5)") == "7"
    assert evaluate("(22+5)") == "27"
    assert evaluate("(-1+5)") == "4"


def test_evaluate_subtraction():
    assert evaluate("2-2") == "0"
    assert evaluate("(2-5)") == "-3"
    assert evaluate("22-5") == "17"
    assert evaluate("(-1-5)") == "-6"


def test_evaluate_multiplcation():
    assert evaluate("2*2") == "4"
    assert evaluate("(2*5)") == "10"
    assert evaluate("2(22+5)") == "54"
    assert evaluate("(-1*5)") == "-5"


def test_evaluate_division():
    assert evaluate("2/2") == "1"
    assert evaluate("(10/5)") == "2"
    assert evaluate("(-1/5)") == "-0.2"


def test_evaluate_exponent():
    assert evaluate("2^2") == "4"
    assert evaluate("(10^5)") == "100000"
    assert evaluate("(-1^5)") == "-1"


def test_evaluate_brackets():
    assert evaluate("(2*2)(2*2)") == "16"
    assert evaluate("3(2*2)(2*2)") == "48"
    assert evaluate("-5(2*2)(2*2)") == "-80"
    assert evaluate("-5(2*2)(2*2)3") == "-240"
    assert evaluate("-5*(2*2)(2*2)*3") == "-240"
    assert evaluate("-5*(22*2)(2*33)*3") == "-43560"


def test_evaluate_decimals():
    assert evaluate("10000000/2*5+6.5") == "25000006.5"
    assert evaluate("5*5.33/5.4+5-1(8.01+8)/2") == "1.930185185185185185185185185"


def test_evaluate_all_operators():
    assert evaluate("5(2*2)(2*2)3-6^2") == "204"
    assert evaluate("5(2*2)(2*2)+3-6^2") == "47"
    assert evaluate("5+(2*2)(2*2)+3-6^2") == "-12"
    assert evaluate("5(2*2)+(2*2)3-6^2") == "-4"
    assert evaluate("-(2*2)-(3^2-3)/4") == "-5.5"


def test_evaluate_fractions():
    assert evaluate("1/3") == "0.3333333333333333333333333333"
    assert evaluate("(1/3)*2") == "0.6666666666666666666666666666"


def test_no_closing_bracket_raise_error():
    with pytest.raises(ValueError):
        evaluate("(1/3")


def test_no_opening_bracket_raise_error():
    with pytest.raises(ValueError):
        evaluate("1+3)")


def test_divide_by_zero():
    with pytest.raises(ValueError):
        evaluate("1/0")


def test_non_binary_expressions():
    with pytest.raises(ValueError):
        evaluate("--1")

    with pytest.raises(ValueError):
        evaluate("2+")

    with pytest.raises(ValueError):
        evaluate("6/")

    with pytest.raises(ValueError):
        evaluate("6*")

    with pytest.raises(ValueError):
        evaluate("(6+5)*5/")

    with pytest.raises(ValueError):
        evaluate("5+5/+2")


def test_non_operators():
    with pytest.raises(ValueError):
        evaluate("1#1")
