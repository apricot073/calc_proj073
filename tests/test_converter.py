import pytest

from toolkit.converter import convert
from toolkit.errors import ConvError


# length

def test_m_to_cm():
    assert convert(1, "m", "cm") == pytest.approx(100.0)


def test_cm_to_m():
    assert convert(100, "cm", "m") == pytest.approx(1.0)


def test_km_to_m():
    assert convert(1, "km", "m") == pytest.approx(1000.0)


def test_mm_to_cm():
    assert convert(10, "mm", "cm") == pytest.approx(1.0)


# weight

def test_kg_to_g():
    assert convert(1, "kg", "g") == pytest.approx(1000.0)


def test_g_to_kg():
    assert convert(1000, "g", "kg") == pytest.approx(1.0)


# temperature

def test_c_to_f():
    assert convert(100, "c", "f") == pytest.approx(212.0)


def test_f_to_c():
    assert convert(212, "f", "c") == pytest.approx(100.0)


def test_c_to_k():
    assert convert(0, "c", "k") == pytest.approx(273.15)


def test_k_to_c():
    assert convert(273.15, "k", "c") == pytest.approx(0.0)


# character case

def test_case_insensitive_from():
    assert convert(1, "M", "CM") == pytest.approx(100.0)


def test_case_insensitive_to():
    assert convert(1, "m", "Km") == pytest.approx(0.001)


# return float

def test_returns_float():
    result = convert(1, "m", "cm")
    assert isinstance(result, float)


# negative tests

def test_unknown_unit():
    with pytest.raises(ConvError):
        convert(5, "xyz", "m")


def test_incompatible_units():
    with pytest.raises(ConvError):
        convert(5, "m", "kg")


def test_below_zero_c():
    with pytest.raises(ConvError):
        convert(-300, "c", "f")


def test_below_zero_k():
    with pytest.raises(ConvError):
        convert(-1, "k", "c")


def test_below_zero_f():
    with pytest.raises(ConvError):
        convert(-500, "f", "c")
