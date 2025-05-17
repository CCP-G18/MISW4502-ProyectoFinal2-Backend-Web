import os
import uuid
import pytest
from datetime import datetime, date
from unittest.mock import patch, MagicMock
from flask import Flask
from app.services.visit_service import VisitService
from app.exceptions.http_exceptions import BadRequestError, NotFoundError
from app.repositories.visit_repository import VisitRepository
from app.models.visit_model import VisitSchema, Visit
from app.core.database import init_db

@pytest.fixture
def visit_data():
    return {
        "observations": "Cliente mostró interés en el nuevo producto.",
        "register_date": date.today(),
        "customer_id": str(uuid.uuid4()),
        "seller_id": str(uuid.uuid4())
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
def visit_schema():
    return VisitSchema()

@pytest.fixture
def visits_schema():
    return VisitSchema(many=True)

def test_create_visit_missing_observations(visit_data):
    del visit_data['observations']
    with pytest.raises(BadRequestError, match="Las observaciones son requeridas"):
        VisitService.create(visit_data)

def test_create_visit_missing_register_date(visit_data):
    del visit_data['register_date']
    with pytest.raises(BadRequestError, match="La fecha de registro es requerida"):
        VisitService.create(visit_data)

def test_create_visit_missing_customer_id(visit_data):
    del visit_data['customer_id']
    with pytest.raises(BadRequestError, match="El id del cliente es requerido"):
        VisitService.create(visit_data)

def test_create_visit_missing_seller_id(visit_data):
    del visit_data['seller_id']
    with pytest.raises(BadRequestError, match="El id del vendedor es requerido"):
        VisitService.create(visit_data)

def test_create_visit_invalid_customer_id(visit_data):
    visit_data['customer_id'] = 'invalid-uuid'
    with pytest.raises(BadRequestError, match="El id del cliente no es válido"):
        VisitService.create(visit_data)

def test_create_visit_invalid_seller_id(visit_data):
    visit_data['seller_id'] = 'invalid-uuid'
    with pytest.raises(BadRequestError, match="El id del vendedor no es válido"):
        VisitService.create(visit_data)

def test_create_visit_register_date_not_today(visit_data):
    from datetime import timedelta

    visit_data['register_date'] = date.today() - timedelta(days=1)
    with pytest.raises(BadRequestError, match="La fecha de registro debe ser hoy"):
        VisitService.create(visit_data)

def test_get_by_id_customer_invalid_customer_id():
    invalid_id = "invalid-uuid"
    with pytest.raises(BadRequestError, match=VisitService.INVALID_ID_CUSTOMER_FORMAT_MESSAGE):
        VisitService.get_by_id_customer(invalid_id)

def test_get_by_id_customer_success(visit_data, app):
    with app.app_context():
        VisitService.create(visit_data)
        visits = VisitService.get_by_id_customer(visit_data["customer_id"])

        assert isinstance(visits, list)
        assert len(visits) >= 1

        visit = visits[0]
        assert visit.customer_id == uuid.UUID(visit_data["customer_id"])
        assert visit.seller_id == uuid.UUID(visit_data["seller_id"])
        assert visit.observations == visit_data["observations"]

def test_create_visit_success(app, visit_data, visit_schema):
    with app.app_context():
        visit = VisitService.create(visit_data)

        result = visit_schema.dump(visit)
        assert result["id"]
        assert result["created_at"]
        assert result["updated_at"]
        assert result["observations"] == visit_data["observations"]
        assert result["customer_id"] == visit_data["customer_id"]
        assert result["seller_id"] == visit_data["seller_id"]
        assert result["register_date"] == visit_data["register_date"].isoformat()

def test_get_all_visits_success(app, visit_data, visits_schema, visit_schema):
    with app.app_context():
        test_create_visit_success(app, visit_data, visit_schema)
        visits = VisitService.get_all()

        result = visits_schema.dump(visits)
        assert result[0]["id"]
        assert result[0]["created_at"]
        assert result[0]["updated_at"]
        assert result[0]["observations"] == visit_data["observations"]
        assert result[0]["customer_id"] == visit_data["customer_id"]
        assert result[0]["seller_id"] == visit_data["seller_id"]

def test_get_visit_by_id_success(app, visit_data, visit_schema):
    with app.app_context():
        visit = VisitService.create(visit_data)
        result = visit_schema.dump(visit)
        found_visit = VisitService.get_by_id(result["id"])

        result = visit_schema.dump(found_visit)

        assert uuid.UUID(result["id"]) == visit.id
        assert result["observations"] == visit_data["observations"]
        assert result["customer_id"] == visit_data["customer_id"]
        assert result["seller_id"] == visit_data["seller_id"]

@patch('app.repositories.visit_repository.VisitRepository.get_all')
def test_get_all_success(mock_get_all):
    mock_get_all.return_value = [MagicMock(id=uuid.uuid4()), MagicMock(id=uuid.uuid4())]

    visits = VisitService.get_all()

    assert len(visits) == 2
    mock_get_all.assert_called_once()

@patch('app.repositories.visit_repository.VisitRepository.get_all')
def test_get_all_no_visits(mock_get_all):
    mock_get_all.return_value = []

    with pytest.raises(ValueError, match="No hay visitas registradas"):
        VisitService.get_all()

@patch('app.repositories.visit_repository.VisitRepository.get_by_id')
def test_get_by_id_success(mock_get_by_id):
    visit_id = str(uuid.uuid4())
    mock_visit = MagicMock(id=uuid.UUID(visit_id))
    mock_get_by_id.return_value = mock_visit

    visit = VisitService.get_by_id(visit_id)

    assert visit == mock_visit
    mock_get_by_id.assert_called_once_with(visit_id)

def test_get_by_id_invalid_uuid():
    invalid_id = "not-a-uuid"
    with pytest.raises(BadRequestError, match=VisitService.INVALID_ID_FORMAT_MESSAGE):
        VisitService.get_by_id(invalid_id)

@patch('app.repositories.visit_repository.VisitRepository.get_by_id')
def test_get_by_id_not_found(mock_get_by_id):
    valid_id = str(uuid.uuid4())
    mock_get_by_id.return_value = None

    with pytest.raises(NotFoundError, match=VisitService.NOT_FOUND_MESSAGE):
        VisitService.get_by_id(valid_id)

@patch('app.repositories.visit_repository.VisitRepository.get_by_id_customer')
def test_get_by_id_customer_success(mock_get_by_id_customer, visit_data):
    mock_visits = [MagicMock(id=uuid.uuid4()), MagicMock(id=uuid.uuid4())]
    mock_get_by_id_customer.return_value = mock_visits

    visits = VisitService.get_by_id_customer(visit_data["customer_id"])

    assert visits == mock_visits
    mock_get_by_id_customer.assert_called_once_with(visit_data["customer_id"])

@patch('app.repositories.visit_repository.VisitRepository.get_by_id_customer')
def test_get_by_id_customer_no_visits(mock_get_by_id_customer):
    valid_customer_id = str(uuid.uuid4())
    mock_get_by_id_customer.return_value = []

    with pytest.raises(NotFoundError, match="No hay visitas registradas"):
        VisitService.get_by_id_customer(valid_customer_id)

@patch('app.repositories.visit_repository.VisitRepository.create')
def test_create_success(mock_create, visit_data):
    mock_visit = MagicMock()
    mock_create.return_value = mock_visit

    visit = VisitService.create(visit_data)

    assert visit == mock_visit
    mock_create.assert_called_once()

def test_create_invalid_register_date_format(visit_data):
    visit_data["register_date"] = "2023/05/15"  # formato inválido
    with pytest.raises(BadRequestError, match="La fecha de registro no tiene un formato válido"):
        VisitService.create(visit_data)

def test_create_register_date_wrong_type(visit_data):
    visit_data["register_date"] = 12345  # tipo inválido
    with pytest.raises(BadRequestError, match="La fecha de registro debe ser un date o un string ISO"):
        VisitService.create(visit_data)
