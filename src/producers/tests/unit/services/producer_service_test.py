import os
import uuid
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.services.producer_service import ProducerService, is_valid_email
from app.exceptions.http_exceptions import BadRequestError
from app.repositories.producer_repository import ProducerRepository
from app.models.producer_model import ProducerSchema, Producer
from app.core.database import init_db

@pytest.fixture
def producer_data():
    return {
        "name": "David Diaz",
        "country": "España",
        "email": "David.Diaz@hotmail.com",
        "address": "8415 Howell Field",
        "phone": "371-797-6480",
        "website": "https://daviddiaz.com",
        "contact_name": "Tony",
        "contact_lastname": "Corkery",
        "contact_email": "Jazmin.Yost@hotmail.com",
        "contact_phone": "1-555-555-4875"
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
def producer_schema():
  return ProducerSchema()

@pytest.fixture
def producers_schema():
  return ProducerSchema(many=True)

def test_valid_email():
  assert is_valid_email("test@example.com")
  assert not is_valid_email("invalid-email")

def test_create_producer_missing_name(producer_data):
    del producer_data['name']
    with pytest.raises(BadRequestError, match="El nombre es requerido"):
        ProducerService.create(producer_data)

def test_create_producer_missing_country(producer_data):
    del producer_data['country']
    with pytest.raises(BadRequestError, match="El país es requerido"):
        ProducerService.create(producer_data)

def test_create_producer_missing_email(producer_data):
    del producer_data['email']
    with pytest.raises(BadRequestError, match="El email es requerido"):
        ProducerService.create(producer_data)

def test_create_producer_missing_address(producer_data):
    del producer_data['address']
    with pytest.raises(BadRequestError, match="La direccion es requerida"):
        ProducerService.create(producer_data)

def test_create_producer_missing_phone(producer_data):
    del producer_data['phone']
    with pytest.raises(BadRequestError, match="El telefono es requerido"):
        ProducerService.create(producer_data)

def test_create_producer_missing_website(producer_data):
    del producer_data['website']
    with pytest.raises(BadRequestError, match="El sitio web es requerido"):
        ProducerService.create(producer_data)

def test_create_producer_missing_contact_name(producer_data):
    del producer_data['contact_name']
    with pytest.raises(BadRequestError, match="El nombre del contacto es requerido"):
        ProducerService.create(producer_data)

def test_create_producer_missing_contact_lastname(producer_data):
    del producer_data['contact_lastname']
    with pytest.raises(BadRequestError, match="El apellido del contacto es requerido"):
        ProducerService.create(producer_data)

def test_create_producer_missing_contact_email(producer_data):
    del producer_data['contact_email']
    with pytest.raises(BadRequestError, match="El email del contacto es requerido"):
        ProducerService.create(producer_data)

def test_create_producer_missing_contact_phone(producer_data):
    del producer_data['contact_phone']
    with pytest.raises(BadRequestError, match="El telefono del contacto es requerido"):
        ProducerService.create(producer_data)

def test_create_producer_invalid_email(producer_data):
    producer_data['email'] = 'invalid-email'
    with pytest.raises(BadRequestError, match="El email no es válido"):
        ProducerService.create(producer_data)

def test_create_producer_success(app, producer_data, producer_schema):

    with app.app_context():
        producer = ProducerService.create(producer_data)

        result = producer_schema.dump(producer)
        assert result["id"]
        assert result["created_at"]
        assert result["updated_at"]
        assert result["name"] == producer_data["name"]
        assert result["country"] == producer_data["country"]
        assert result["email"] == producer_data["email"]

def test_get_all_success(app, producer_data, producers_schema, producer_schema):
    with app.app_context():
        test_create_producer_success(app, producer_data, producer_schema)
        producers = ProducerService.get_all()

        result = producers_schema.dump(producers)
        assert result[0]["id"]
        assert result[0]["created_at"]
        assert result[0]["updated_at"]
        assert result[0]["name"] == producer_data["name"]
        assert result[0]["country"] == producer_data["country"]
        assert result[0]["email"] == producer_data["email"]

def test_get_by_id_success(app, producer_data, producer_schema):
    with app.app_context():
        producer = ProducerService.create(producer_data)
        result = producer_schema.dump(producer)
        found_producer = ProducerService.get_by_id(result["id"])

        result = producer_schema.dump(found_producer)
        
        assert uuid.UUID(result["id"]) == producer.id
        assert result["name"] == producer_data["name"]
        assert result["country"] == producer_data["country"]
        assert result["email"] == producer_data["email"]