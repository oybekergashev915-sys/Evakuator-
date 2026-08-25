import pytest

from utils import calculate_price, format_money, validate_km, validate_positive_int


# ---------- calculate_price ----------

def test_calculate_price_basic():
    assert calculate_price(10, 10000) == 100000


def test_calculate_price_zero_km():
    assert calculate_price(0, 10000) == 0


def test_calculate_price_fractional_km():
    assert calculate_price(2.5, 10000) == 25000


def test_calculate_price_rounding():
    assert calculate_price(2.449, 1000) == 2449


def test_calculate_price_large_km():
    assert calculate_price(2999, 20000) == 2999 * 20000


def test_calculate_price_negative_km():
    assert calculate_price(-5, 10000) == -50000


# ---------- validate_km ----------

def test_validate_km_valid_integer():
    assert validate_km("45") == 45.0


def test_validate_km_valid_with_spaces():
    assert validate_km(" 12.5 ") == 12.5


def test_validate_km_valid_with_comma():
    assert validate_km("12,5") == 12.5


def test_validate_km_zero_rejected():
    with pytest.raises(ValueError):
        validate_km("0")


def test_validate_km_negative_rejected():
    with pytest.raises(ValueError):
        validate_km("-10")


def test_validate_km_not_a_number():
    with pytest.raises(ValueError):
        validate_km("abc")


def test_validate_km_too_large():
    with pytest.raises(ValueError):
        validate_km("5000")


def test_validate_km_max_boundary_ok():
    assert validate_km("3000") == 3000.0


def test_validate_km_custom_max():
    with pytest.raises(ValueError):
        validate_km("150", max_km=100)


# ---------- validate_positive_int ----------

def test_validate_positive_int_ok():
    assert validate_positive_int("350000") == 350000


def test_validate_positive_int_rejects_zero():
    with pytest.raises(ValueError):
        validate_positive_int("0")


def test_validate_positive_int_rejects_negative():
    with pytest.raises(ValueError):
        validate_positive_int("-100")


def test_validate_positive_int_rejects_float():
    with pytest.raises(ValueError):
        validate_positive_int("10.5")


def test_validate_positive_int_rejects_text():
    with pytest.raises(ValueError):
        validate_positive_int("abc")


# ---------- format_money ----------

def test_format_money_thousands_separator():
    assert format_money(350000) == "350 000 сум"


def test_format_money_small_number():
    assert format_money(500) == "500 сум"
