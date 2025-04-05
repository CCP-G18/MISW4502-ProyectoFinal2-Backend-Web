import os
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.services.seller_service import SellerService, is_valid_email
from app.exceptions.http_exceptions import BadRequestError
from app.repositories.seller_repository import SellerRepository
from app.models.seller_model import SellerSchema, Seller

os.environ['PATH_API_USER'] = 'http://mocked_api/users'
os.environ['PASSWORD_DEFAULT'] = 'password123'

@pytest.fixture
def seller_data():
  return {
    "name": "Juan",
    "lastname": "Perez",
    "email": "juan.perez@example.com",
    "assignedArea": "North"
  }
@pytest.fixture
def app():
  app = Flask(__name__)
  app.config['TESTING'] = True
  return app

@pytest.fixture
def client(app):
  return app.test_client()

@pytest.fixture
def mock_seller():
  return Seller(
    assigned_area="North",
    user_id="abc12345-1234-5678-8901-abcdefabcdef",
  )
@pytest.fixture
def seller_schema():
  return SellerSchema()

@pytest.fixture
def mock_sellers(mock_seller):
  return [mock_seller]

def test_valid_email():
  assert is_valid_email("test@example.com")
  assert not is_valid_email("invalid-email")

def test_create_seller_missing_name(seller_data):
  del seller_data['name']
  with pytest.raises(BadRequestError, match="El nombre es requerido"):
    SellerService.create(seller_data)

def test_create_seller_missing_lastname(seller_data):
  del seller_data['lastname']
  with pytest.raises(BadRequestError, match="El apellido es requerido"):
    SellerService.create(seller_data)

def test_create_seller_missing_email(seller_data):
  del seller_data['email']
  with pytest.raises(BadRequestError, match="El email es requerido"):
    SellerService.create(seller_data)

def test_create_seller_invalid_email(seller_data):
  seller_data['email'] = 'invalid-email'
  with pytest.raises(BadRequestError, match="El email no es válido"):
    SellerService.create(seller_data)

@patch.dict(os.environ, {'PATH_API_USER': 'http://mocked_api/users', 'PASSWORD_DEFAULT': 'password123'})
@patch('requests.post')
@patch.object(SellerRepository, 'create', return_value={"id": "mocked-id"})
def test_create_seller_success(mock_create, mock_post, seller_data):
  mock_response = MagicMock()
  mock_response.status_code = 201
  mock_response.json.return_value = {"data": {"id": "mocked-id"}}
  mock_post.return_value = mock_response

  SellerService.BASE_URL_USER_API = os.getenv('PATH_API_USER')
  SellerService.PASSWORD_DEFAULT = os.getenv('PASSWORD_DEFAULT')

  result = SellerService.create(seller_data)

  assert result["id"] == "mocked-id"
  mock_post.assert_called_once_with(
    'http://mocked_api/users',
    json={
      "name": "Juan",
      "lastname": "Perez",
      "email": "juan.perez@example.com",
      "password": 'password123',
      "role": "seller"
    }
  )
  mock_create.assert_called_once_with({
    "assigned_area": "North",
    "user_id": "mocked-id"
  })

@patch('requests.post')
def test_create_seller_external_api_failure(mock_post, seller_data):
  mock_response = MagicMock()
  mock_response.status_code = 400
  mock_response.json.return_value = {"error": "Error de creación de usuario"}
  mock_post.return_value = mock_response

  with pytest.raises(BadRequestError, match="Error de creación de usuario"):
    SellerService.create(seller_data)


@patch('app.repositories.seller_repository.SellerRepository.get_all')
@patch('requests.get')
def test_get_all_success(mock_requests_get, mock_get_all, mock_sellers, seller_schema, client):
  mock_get_all.return_value = mock_sellers

  response_data = {
    "data": {
      "name": "Juan",
      "lastname": "Perez",
      "email": "juan.perez@example.com"
    }
  }
  mock_requests_get.return_value = MagicMock(status_code=200, json=lambda: response_data)

  with client.application.test_request_context(headers={"Authorization": "Bearer test_token"}):
      
    sellers_dict = SellerService.get_all()

    mock_requests_get.assert_called_once_with(
      f'{SellerService.BASE_URL_USER_API}/abc12345-1234-5678-8901-abcdefabcdef',
      headers={'Authorization': 'Bearer test_token'}
    )

    assert len(sellers_dict) == 1
    assert sellers_dict[0]['name'] == "Juan Perez"
    assert sellers_dict[0]['email'] == "juan.perez@example.com"
    
@patch('app.repositories.seller_repository.SellerRepository.get_all')
@patch('requests.get')
def test_get_all_failure(mock_requests_get, mock_get_all, mock_sellers, seller_schema, client):
  mock_get_all.return_value = mock_sellers

  mock_requests_get.return_value = MagicMock(status_code=404, json=lambda: {"message": "User not found"})

  with client.application.test_request_context(headers={"Authorization": "Bearer test_token"}):
        
    with pytest.raises(BadRequestError) as exc_info:
      SellerService.get_all()
      assert str(exc_info.value) == "No se pudo obtener el vendedor"
      
@patch('app.repositories.seller_repository.SellerRepository.get_all')
def test_get_all_no_sellers(mock_get_all, client):
  mock_get_all.return_value = []

  with client.application.test_request_context(headers={"Authorization": "Bearer test_token"}):
    with pytest.raises(BadRequestError) as exc_info:
      SellerService.get_all()

      assert str(exc_info.value) == "No hay vendedores registrados"