import pytest

from toolkit.converter import Convert
from toolkit.errors import ConvError


# length

def test_m_to_cm():
    assert Convert(1, "m", "cm") == pytest.approx(100.0)


def test_cm_to_m():
    assert Convert(100, "cm", "m") == pytest.approx(1.0)


def test_km_to_m():
    assert Convert(1, "km", "m") == pytest.approx(1000.0)


def test_mm_to_cm():
    assert Convert(10, "mm", "cm") == pytest.approx(1.0)


# weight

def test_kg_to_g():
    assert Convert(1, "kg", "g") == pytest.approx(1000.0)


def test_g_to_kg():
    assert Convert(1000, "g", "kg") == pytest.approx(1.0)


# temperature

def test_c_to_f():
    assert Convert(100, "c", "f") == pytest.approx(212.0)


def test_f_to_c():
    assert Convert(212, "f", "c") == pytest.approx(100.0)


def test_c_to_k():
    assert Convert(0, "c", "k") == pytest.approx(273.15)


def test_k_to_c():
    assert Convert(273.15, "k", "c") == pytest.approx(0.0)


# character case

def test_case_insensitive_from():
    assert Convert(1, "M", "CM") == pytest.approx(100.0)


def test_case_insensitive_to():
    assert Convert(1, "m", "Km") == pytest.approx(0.001)


# return float

def test_returns_float():
    result = Convert(1, "m", "cm")
    assert isinstance(result, float)


# negative tests

def test_unknown_unit():
    with pytest.raises(ConvError):
        Convert(5, "xyz", "m")


def test_incompatible_units():
    with pytest.raises(ConvError):
        Convert(5, "m", "kg")


def test_below_zero_c():
    with pytest.raises(ConvError):
        Convert(-300, "c", "f")


def test_below_zero_k():
    with pytest.raises(ConvError):
        Convert(-1, "k", "c")


def test_below_zero_f():
    with pytest.raises(ConvError):
        Convert(-500, "f", "c")
