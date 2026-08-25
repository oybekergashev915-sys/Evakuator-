def format_money(amount: int) -> str:
    return f"{amount:,.0f}".replace(",", " ") + " сум"


def format_km(km: float) -> str:
    if float(km).is_integer():
        return str(int(km))
    return f"{km:.1f}"


def calculate_price(km: float, price_per_km: int) -> int:
    return round(km * price_per_km)


def validate_km(text: str, max_km: int = 3000) -> float:
    if text is None:
        raise ValueError("Введите число.")

    normalized = text.strip().replace(",", ".")
    try:
        km = float(normalized)
    except ValueError:
        raise ValueError(
            "Это не похоже на число. Введите расстояние в километрах, например: 45"
        )

    if km != km or km in (float("inf"), float("-inf")):
        raise ValueError("Некорректное значение.")
    if km <= 0:
        raise ValueError("Расстояние должно быть положительным числом.")
    if km > max_km:
        raise ValueError(f"Расстояние слишком большое (максимум {max_km} км).")

    return km


def validate_positive_int(text: str, field_name: str = "значение") -> int:
    try:
        value = int((text or "").strip())
    except ValueError:
        raise ValueError(
            f"Введите целое положительное число для поля «{field_name}»."
        )

    if value <= 0:
        raise ValueError(f"Значение поля «{field_name}» должно быть положительным числом.")

    return value
