import pytest
from unittest.mock import patch, MagicMock
from app.services.order_service import OrderService
from app.exceptions.http_exceptions import BadRequestError, NotFoundError


@patch("app.repositories.order_repository.OrderRepository.get_all")
def test_get_all_orders_success(mock_get_all):
    mock_get_all.return_value = [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "customer_id": "123e4567-e89b-12d3-a456-426614174001",
            "total_amount": 100.0,
            "state": "PREPARING",
            "delivery_date": "2025-05-01"
        }
    ]

    result = OrderService.get_all()

    assert len(result) == 1
    assert result[0]["id"] == "123e4567-e89b-12d3-a456-426614174000"
    assert result[0]["customer_id"] == "123e4567-e89b-12d3-a456-426614174001"
    assert result[0]["total_amount"] == 100.0
    assert result[0]["state"] == "PREPARING"
    assert result[0]["delivery_date"] == "2025-05-01"


@patch("app.repositories.order_repository.OrderRepository.get_by_id")
def test_get_order_by_id_success(mock_get_by_id):
    mock_get_by_id.return_value = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "customer_id": "123e4567-e89b-12d3-a456-426614174001",
        "total_amount": 100.0,
        "state": "PREPARING",
        "delivery_date": "2025-05-01"
    }

    result = OrderService.get_by_id("123e4567-e89b-12d3-a456-426614174000")

    assert result["id"] == "123e4567-e89b-12d3-a456-426614174000"
    assert result["customer_id"] == "123e4567-e89b-12d3-a456-426614174001"
    assert result["total_amount"] == 100.0
    assert result["state"] == "PREPARING"
    assert result["delivery_date"] == "2025-05-01"


@patch("app.repositories.order_repository.OrderRepository.get_by_id")
def test_get_order_by_id_not_found(mock_get_by_id):
    mock_get_by_id.return_value = None

    with pytest.raises(NotFoundError, match="Pedido no encontrado"):
        OrderService.get_by_id("123e4567-e89b-12d3-a456-426614174000")

@patch("app.repositories.order_repository.OrderRepository.get_by_id")
def test_get_order_by_id_invalid(mock_get_by_id):
    mock_get_by_id.return_value = None

    with pytest.raises(BadRequestError, match=" El formato del id del pedido no es correcto"):
        OrderService.get_by_id("123e4567-e89b-12d3-a456")

@patch("app.repositories.order_repository.OrderRepository.create")
def test_create_order_missing_date(mock_create):
    order_data = {
        "items": [
            {"product_id": "123e4567-e89b-12d3-a456-426614174002", "quantity": 2}
        ]
    }
    customer_id = "123e4567-e89b-12d3-a456-426614174001"

    with pytest.raises(BadRequestError, match="El campo 'date' es obligatorio"):
        OrderService.create_order(customer_id, order_data)

@patch("app.repositories.order_repository.OrderRepository.create")
def test_create_order_missing_items(mock_create):
    order_data = {
        "date": "2025-05-27",
        "total": 250000.0
    }
    customer_id = "123e4567-e89b-12d3-a456-426614174001"

    with pytest.raises(BadRequestError, match="La petición debe contener una lista de productos válida"):
        OrderService.create_order(customer_id, order_data)