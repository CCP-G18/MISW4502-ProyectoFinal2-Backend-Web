import pytest
from datetime import date
from app.utils.delivery_date_util import get_delivery_date

def test_get_delivery_date_start_on_weekday():
    start_date = "2025-04-28"  # Lunes
    result = get_delivery_date(start_date, days=2)
    assert result == date(2025, 4, 30)  # Miércoles

def test_get_delivery_date_start_on_weekend():
    start_date = "2025-04-26"  # Sábado
    result = get_delivery_date(start_date, days=2)
    assert result == date(2025, 4, 29)  # Miércoles

def test_get_delivery_date_with_default_days():
    start_date = "2025-04-28"  # Lunes
    result = get_delivery_date(start_date)
    assert result == date(2025, 4, 30)  # Miércoles

def test_get_delivery_date_with_custom_days():
    start_date = "2025-04-28"  # Lunes
    result = get_delivery_date(start_date, days=5)
    assert result == date(2025, 5, 5)  # Lunes siguiente

def test_get_delivery_date_invalid_date_format():
    start_date = "28-04-2025"
    with pytest.raises(ValueError, match="time data '28-04-2025' does not match format '%Y-%m-%d'"):
        get_delivery_date(start_date)

def test_get_delivery_date_start_as_date_object():
    start_date = date(2025, 4, 28)  # Lunes
    result = get_delivery_date(start_date, days=3)
    assert result == date(2025, 5, 1)  # Jueves