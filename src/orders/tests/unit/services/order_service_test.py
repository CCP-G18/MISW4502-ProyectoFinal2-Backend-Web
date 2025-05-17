from flask import json
import pytest
import os
from unittest.mock import patch, MagicMock
from app.services.order_service import OrderService
from app.exceptions.http_exceptions import BadRequestError, NotFoundError

@pytest.fixture
def order_service():
    return OrderService()

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def mock_update_product_stock():
    with patch("app.services.order_service.update_product_stock") as mock:
        yield mock

@patch("app.repositories.order_repository.OrderRepository.get_all")
@patch.dict(os.environ, {"PATH_API_USER": "http://user_app:5000/users"})
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

@patch("app.repositories.order_repository.OrderRepository.get_all")
def test_get_all_orders_without_data(mock_get_all):
    mock_get_all.return_value = []

    with pytest.raises(ValueError, match="No hay pedidos registrados"):
        OrderService.get_all()

@patch("app.repositories.order_repository.OrderRepository.get_by_id")
def test_get_order_by_id_invalid(mock_get_by_id):
    mock_get_by_id.return_value = None

    with pytest.raises(BadRequestError, match="El formato del id del pedido no es correcto"):
        OrderService.get_by_id("123e4567-e89b-12d3-a456")

@patch("app.repositories.order_repository.OrderRepository.get_by_id")
def test_get_order_by_id_not_found(mock_get_by_id):    
    mock_get_by_id.return_value = None

    with pytest.raises(NotFoundError, match="Pedido no encontrado"):
        OrderService.get_by_id("123e4567-e89b-12d3-a456-426614174000")        

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

@patch("app.repositories.order_repository.OrderRepository.create")
def test_create_order_missing_date(mock_create_order):
    order_data = {
        "items": [
            {"id": "123e4567-e89b-12d3-a456-426614174002", "quantity": 2}
        ]
    }
    customer_id = "123e4567-e89b-12d3-a456-426614174001"
    with pytest.raises(BadRequestError, match="El campo 'date' es obligatorio"):
        OrderService.create_order(customer_id, order_data)

@patch("app.repositories.order_repository.OrderRepository.create")
def test_create_order_missing_items(mock_create_order):
    order_data = {
        "date": "2025-05-01"
    }
    customer_id = "123e4567-e89b-12d3-a456-426614174001"
    with pytest.raises(BadRequestError, match="a petición debe contener una lista de productos válida"):
        OrderService.create_order(customer_id, order_data)

@patch("app.repositories.order_repository.OrderRepository.create")
def test_create_order_missing_items_list(mock_create_order):
    order_data = {
        "date": "2025-05-01",
        "items": "not_a_list"
    }
    customer_id = "123e4567-e89b-12d3-a456-426614174001"
    with pytest.raises(BadRequestError, match="a petición debe contener una lista de productos válida"):
        OrderService.create_order(customer_id, order_data)

@patch("app.services.order_service.get_product_info")
def test_validate_products_product_not_found(mock_get_product_info):
    mock_get_product_info.return_value = None

    items = [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "quantity": 2
        }
    ]

    with pytest.raises(NotFoundError, match="Producto con ID 123e4567-e89b-12d3-a456-426614174000 no encontrado"):
        OrderService.validate_products(items)

@patch("app.services.order_service.validate_uuid")
def test_validate_products_invalid_product_id(mock_validate_uuid):
    mock_validate_uuid.return_value = False

    items = [
        {"id": "invalid-uuid", "quantity": 2}
    ]

    with pytest.raises(BadRequestError, match="El ID del producto no es válido"):
        OrderService.validate_products(items)

    mock_validate_uuid.assert_called_once_with("invalid-uuid")

@patch("app.services.order_service.get_product_info")
def test_validate_products_without_product_id(mock_get_product_info):
    mock_get_product_info.return_value = None

    items = [
        {"quantity": 2}
    ]

    with pytest.raises(BadRequestError, match="Cada producto debe incluir 'id' y 'quantity'"):
        OrderService.validate_products(items)

@patch("app.services.order_service.get_product_info")
def test_validate_products_without_quantity(mock_get_product_info):
    mock_get_product_info.return_value = None

    items = [
        {"id": "123e4567-e89b-12d3-a456-426614174000"}
    ]

    with pytest.raises(BadRequestError, match="Cada producto debe incluir 'id' y 'quantity'"):
        OrderService.validate_products(items)

@patch("app.services.order_service.get_product_info")
def test_validate_products_negative_quantity(mock_get_product_info):
    mock_get_product_info.return_value = None

    items = [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "quantity": -1
        }]

    with pytest.raises(BadRequestError, match="La cantidad debe ser un número entero positivo"):
        OrderService.validate_products(items)

@patch("app.services.order_service.get_product_info")
def test_validate_products_invalid_quantity(mock_get_product_info):
    mock_get_product_info.return_value = None

    items = [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "quantity": "invalid_quantity"
        }]

    with pytest.raises(BadRequestError, match="La cantidad debe ser un número entero positivo"):
        OrderService.validate_products(items)

@patch("app.services.order_service.get_product_info")
def test_validate_products_success(mock_get_product_info):
    mock_get_product_info.side_effect = [
        {
            "data": {
                "name": "Producto A",
                "quantity": 10,
                "unit_amount": 5000.0,
                "image_url": "https://example.com/producto_a.jpg"
            }
        },
        {
            "data": {
                "name": "Producto B",
                "quantity": 20,
                "unit_amount": 3000.0,
                "image_url": "https://example.com/producto_b.jpg"
            }
        }
    ]

    items = [
        {"id": "123e4567-e89b-12d3-a456-426614174000", "quantity": 2},
        {"id": "123e4567-e89b-12d3-a456-426614174001", "quantity": 3}
    ]
    validated_items, total_amount, summary = OrderService.validate_products(items)

    assert len(validated_items) == 2
    assert total_amount == 19000.0
    assert summary == ["Producto A", "Producto B"]
    
    assert validated_items[0]["quantity"] == 10
    assert validated_items[0]["quantity_ordered"] == 2
    assert validated_items[0]["amount"] == 10000.0
    assert validated_items[0]["name"] == "Producto A"
    assert validated_items[0]["image_url"] == "https://example.com/producto_a.jpg"
    assert validated_items[0]["price"] == 5000.0

    assert validated_items[1]["quantity"] == 20
    assert validated_items[1]["quantity_ordered"] == 3
    assert validated_items[1]["amount"] == 9000.0
    assert validated_items[1]["name"] == "Producto B"
    assert validated_items[1]["image_url"] == "https://example.com/producto_b.jpg"
    assert validated_items[1]["price"] == 3000.0

    mock_get_product_info.assert_any_call("123e4567-e89b-12d3-a456-426614174000")
    mock_get_product_info.assert_any_call("123e4567-e89b-12d3-a456-426614174001")
    assert mock_get_product_info.call_count == 2

@patch("app.services.order_service.get_product_info")
def test_validate_products_insufficient_stock(mock_get_product_info):
    mock_get_product_info.side_effect = [
        {
            "data": {
                "name": "Producto A",
                "quantity": 1,
                "unit_amount": 5000.0,
                "image_url": "https://example.com/producto_a.jpg"
            }
        }
    ]
    items = [
        {"id": "123e4567-e89b-12d3-a456-426614174000", "quantity": 2}
    ]

    with pytest.raises(BadRequestError, match="No hay suficiente cantidad del producto Producto A en stock"):
        OrderService.validate_products(items)

@patch("app.services.order_service.get_product_info")
def test_validate_products_empty_items(mock_get_product_info):
    items = []

    validated_items, total_amount, summary = OrderService.validate_products(items)

    assert len(validated_items) == 0
    assert total_amount == 0.0
    assert summary == []

@patch("app.repositories.order_repository.OrderRepository.get_all")
def test_get_orders_by_customer_invalid_id(mock_get_all):
    invalid_customer_id = "invalid-uuid"

    with pytest.raises(BadRequestError, match="El id del cliente no es válido"):
        OrderService.get_orders_by_customer(invalid_customer_id)

    mock_get_all.assert_not_called()

@patch("app.services.order_service.OrderService.validate_products")
def test_create_order_seller_missing_date(mock_validate_products):  
    seller_id = "123e4567-e89b-12d3-a456-426614174000"
    order_data = {
        "customer_id": "456e7890-e12b-34d5-a678-426614174111",
        "items": [
            {"product_id": "789e1234-e56b-78d9-a012-426614174222", "quantity": 2}
        ]
    }
    with pytest.raises(BadRequestError, match="El campo 'date' es obligatorio"):
        OrderService.create_order_seller(seller_id, order_data)

    mock_validate_products.assert_not_called()

@patch("app.services.order_service.OrderService.validate_products")
def test_create_order_seller_invalid_customer_id(mock_validate_products):
    seller_id = "123e4567-e89b-12d3-a456-426614174000"
    order_data = {
        "customer_id": "invalid-uuid",
        "date": "2025-05-11",
        "items": [
            {"product_id": "789e1234-e56b-78d9-a012-426614174222", "quantity": 2}
        ]
    }
    with pytest.raises(BadRequestError, match="El ID del cliente no es válido"):
        OrderService.create_order_seller(seller_id, order_data)

    mock_validate_products.assert_not_called()

@patch("app.services.order_service.OrderService.validate_products")
def test_create_order_seller_missing_items(mock_validate_products):
    seller_id = "123e4567-e89b-12d3-a456-426614174000"
    order_data = {
        "customer_id": "456e7890-e12b-34d5-a678-426614174111",
        "date": "2025-05-11"
    }

    with pytest.raises(BadRequestError, match="La petición debe contener una lista de productos válida"):
        OrderService.create_order_seller(seller_id, order_data)

    mock_validate_products.assert_not_called()

@patch("app.repositories.order_repository.OrderRepository.get_all")
def test_get_orders_by_customer_invalid_id(mock_get_all):
    invalid_customer_id = "invalid-uuid"

    with pytest.raises(BadRequestError, match="El id del cliente no es válido"):
        OrderService.get_orders_by_customer(invalid_customer_id)

    mock_get_all.assert_not_called()

@patch("app.services.order_service.OrderService.validate_products")
def test_create_order_seller_missing_date(mock_validate_products):  
    seller_id = "123e4567-e89b-12d3-a456-426614174000"
    order_data = {
        "customer_id": "456e7890-e12b-34d5-a678-426614174111",
        "items": [
            {"product_id": "789e1234-e56b-78d9-a012-426614174222", "quantity": 2}
        ]
    }
    with pytest.raises(BadRequestError, match="El campo 'date' es obligatorio"):
        OrderService.create_order_seller(seller_id, order_data)

    mock_validate_products.assert_not_called()

@patch("app.services.order_service.OrderService.validate_products")
def test_create_order_seller_invalid_customer_id(mock_validate_products):
    seller_id = "123e4567-e89b-12d3-a456-426614174000"
    order_data = {
        "customer_id": "invalid-uuid",
        "date": "2025-05-11",
        "items": [
            {"product_id": "789e1234-e56b-78d9-a012-426614174222", "quantity": 2}
        ]
    }
    with pytest.raises(BadRequestError, match="El ID del cliente no es válido"):
        OrderService.create_order_seller(seller_id, order_data)

    mock_validate_products.assert_not_called()

@patch("app.services.order_service.OrderService.validate_products")
def test_create_order_seller_missing_items(mock_validate_products):
    seller_id = "123e4567-e89b-12d3-a456-426614174000"
    order_data = {
        "customer_id": "456e7890-e12b-34d5-a678-426614174111",
        "date": "2025-05-11"
    }

    with pytest.raises(BadRequestError, match="La petición debe contener una lista de productos válida"):
        OrderService.create_order_seller(seller_id, order_data)

    mock_validate_products.assert_not_called()

@patch("app.services.order_service.db.session")
@patch("app.services.order_service.get_product_info")
@patch("app.services.order_service.update_product_quantity")
def test_create_order_success(mock_update_stock, mock_get_info, mock_session, order_service):
    customer_id = "123e4567-e89b-12d3-a456-426614174000"
    order_data = {        
        "date": "2023-01-01",
        "items": [
            {"id": "6b7c8d99-3e4f-5a6b-7c8d-9e1f2a3b4c5d", "quantity": 2},
            {"id": "1d2561f3-9f43-46c9-9af7-b2a43edc1956", "quantity": 1}
        ]
    }

    mock_product_response = {
        "data": {
            "product_id": "dummy-id",
            "name": "Test Product",
            "quantity": 10,
            "unit_amount": 100.0,
            "image_url": "http://example.com/image.png",
            "description": "Descripción del producto"
        }
    }

    mock_get_info.side_effect = [mock_product_response, mock_product_response]
    created_order = order_service.create_order(customer_id, order_data)
    assert created_order["date"] == "2023-01-03"
    assert len(created_order["items"]) == 2
    assert mock_update_stock.call_count == 2
    assert mock_session.begin.called

@patch("app.services.order_service.db.session")
@patch("app.services.order_service.get_product_info")
@patch("app.services.order_service.update_product_quantity")
@patch("app.services.order_service.notify_inventory_update")
def test_create_order_seller_success(mock_notify, mock_update_stock, mock_get_info, mock_session, order_service):
    seller_id = "223e4567-e89b-12d3-a456-426614174111"
    customer_id = "123e4567-e89b-12d3-a456-426614174000"
    order_data = {        
        "date": "2023-01-01",
        "customer_id": customer_id,
        "items": [
            {"id": "6b7c8d99-3e4f-5a6b-7c8d-9e1f2a3b4c5d", "quantity": 2},
            {"id": "1d2561f3-9f43-46c9-9af7-b2a43edc1956", "quantity": 1}
        ]
    }

    mock_product_response = {
        "data": {
            "product_id": "dummy-id",
            "name": "Test Product",
            "quantity": 10,
            "unit_amount": 100.0,
            "image_url": "http://example.com/image.png",
            "description": "Descripción del producto"
        }
    }

    mock_get_info.side_effect = [mock_product_response, mock_product_response]
    created_order = order_service.create_order_seller(seller_id, order_data)
    assert created_order["date"] == "2023-01-03"
    assert len(created_order["items"]) == 2
    assert mock_update_stock.call_count == 2
    assert mock_notify.call_count == 1
    assert mock_session.begin.called