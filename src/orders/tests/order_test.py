import os
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.services.order_service import OrderService
from app.exceptions.http_exceptions import BadRequestError
from app.repositories.order_repository import OrderRepository

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_orders():
    return [
        {
            "id": "order-001",
            "summary": "Papas, Atún, Leche...",
            "date": "2025-05-27",
            "total": 250000.0,
            "status": "PREPARING",
            "items": [
                {"title": "Papas", "quantity": 2, "price": 5000.0, "image_url": "url1"},
                {"title": "Atún", "quantity": 3, "price": 8500.0, "image_url": "url2"},
                {"title": "Leche", "quantity": 4, "price": 3500.0, "image_url": "url3"},
            ]
        }
    ]

@patch('app.repositories.order_repository.OrderRepository.get_all_by_user')
def test_get_orders_success(mock_get_all_by_user, mock_orders, client):
    mock_get_all_by_user.return_value = mock_orders

    with client.application.test_request_context(headers={"Authorization": "Bearer test_token"}):
        orders = OrderService.get_by_user("user-123")

        assert len(orders) == 1
        assert orders[0]["id"] == "order-001"
        assert orders[0]["items"][0]["title"] == "Papas"
        assert orders[0]["status"] == "PREPARING"

@patch('app.repositories.order_repository.OrderRepository.get_all_by_user')
def test_get_orders_empty(mock_get_all_by_user, client):
    mock_get_all_by_user.return_value = []

    with client.application.test_request_context(headers={"Authorization": "Bearer test_token"}):
        with pytest.raises(BadRequestError, match="No hay órdenes registradas"):
            OrderService.get_by_user("user-123")

@patch('app.repositories.order_repository.OrderRepository.get_all_by_user')
def test_get_orders_repository_error(mock_get_all_by_user, client):
    mock_get_all_by_user.side_effect = Exception("Database down")

    with client.application.test_request_context(headers={"Authorization": "Bearer test_token"}):
        with pytest.raises(Exception, match="Database down"):
            OrderService.get_by_user("user-123")
