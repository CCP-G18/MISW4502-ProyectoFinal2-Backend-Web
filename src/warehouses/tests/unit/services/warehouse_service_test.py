import os
import uuid
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.services.warehouse_service import WarehouseService
from app.exceptions.http_exceptions import BadRequestError, NotFoundError
from app.repositories.warehouse_repository import WarehouseRepository
from app.models.warehouse_model import WarehouseSchema, Warehouse
from app.core.database import init_db


@pytest.fixture
def warehouse_data():
    return {
        "name": "Almacen 1",
        "location": "Calle prueba, Bogotá, Colombia",
    }

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'test-secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    init_db(app)

    return app

@pytest.fixture
def client(app):
  return app.test_client()

@pytest.fixture
def warehouse_schema():
    return WarehouseSchema()

@pytest.fixture
def warehouses_schema():
    return WarehouseSchema(many=True)

def get_mock_warehouse(data):
    return Warehouse(
        name=data["name"],
        location=data["location"],
    )

def test_create_warehouse_missing_name(warehouse_data):
    del warehouse_data['name']
    with pytest.raises(BadRequestError, match="El nombre es requerido"):
        WarehouseService.create(warehouse_data)

def test_create_warehouse_missing_location(warehouse_data):
    del warehouse_data['location']
    with pytest.raises(BadRequestError, match="la ubicación es requerida"):
        WarehouseService.create(warehouse_data)

@patch("app.repositories.warehouse_repository.WarehouseRepository.create")
def test_create_warehouse_success(mock_create, app, warehouse_schema, warehouse_data):

    mock_warehouse = Warehouse(
        name=warehouse_data["name"],
        location=warehouse_data["location"],
    )
    mock_create.return_value = mock_warehouse

    with app.app_context():
        warehouse = WarehouseService.create(warehouse_data)
        result = warehouse_schema.dump(warehouse)

    assert result["name"] == warehouse_data["name"]
    assert result["location"] == warehouse_data["location"]

@patch('app.repositories.warehouse_repository.WarehouseRepository.get_all')
def test_get_all_warehouses_success(mock_get_all, warehouse_data, warehouses_schema):
    mock_warehouse = get_mock_warehouse(warehouse_data)
    mock_get_all.return_value = [mock_warehouse]

    warehouses = WarehouseService.get_all()
    result = warehouses_schema.dump(warehouses)

    assert result[0]["name"] == warehouse_data["name"]
    assert result[0]["location"] == warehouse_data["location"]

@patch('app.repositories.warehouse_repository.WarehouseRepository.get_all')
def test_get_all_success(mock_get_all):
    mock_get_all.return_value = [MagicMock(id=uuid.uuid4()), MagicMock(id=uuid.uuid4())]

    warehouses = WarehouseService.get_all()

    assert len(warehouses) == 2
    mock_get_all.assert_called_once()

@patch('app.repositories.warehouse_repository.WarehouseRepository.get_all')
def test_get_all_no_warehouses(mock_get_all):
    mock_get_all.return_value = []

    with pytest.raises(ValueError, match="No hay bodegas registradas"):
        WarehouseService.get_all()

@patch('app.repositories.warehouse_repository.WarehouseRepository.get_by_id')
def test_get_by_id_success(mock_get_by_id):
    warehouse_id = str(uuid.uuid4())
    mock_warehouse = MagicMock(id=uuid.UUID(warehouse_id))
    mock_get_by_id.return_value = mock_warehouse

    warehouse = WarehouseService.get_by_id(warehouse_id)

    assert warehouse == mock_warehouse
    mock_get_by_id.assert_called_once_with(warehouse_id)

def test_get_by_id_invalid_uuid():
    invalid_id = "not-a-uuid"
    with pytest.raises(BadRequestError, match=WarehouseService.INVALID_ID_FORMAT_MESSAGE):
      WarehouseService.get_by_id(invalid_id)

@patch('app.repositories.warehouse_repository.WarehouseRepository.get_by_id')
def test_get_by_id_not_found(mock_get_by_id):
    valid_id = str(uuid.uuid4())
    mock_get_by_id.return_value = None

    with pytest.raises(NotFoundError, match=WarehouseService.NOT_FOUND_MESSAGE):
      WarehouseService.get_by_id(valid_id)


@patch('app.repositories.warehouse_repository.WarehouseRepository.create')
def test_create_success(mock_create, warehouse_data):
    mock_warehouse = MagicMock()
    mock_create.return_value = mock_warehouse

    warehouse = WarehouseService.create(warehouse_data)

    assert warehouse == mock_warehouse
    mock_create.assert_called_once()
