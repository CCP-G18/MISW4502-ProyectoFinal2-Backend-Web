import os
import pytest
from unittest.mock import patch, MagicMock
from app.services.seller_service import SellerService, is_valid_email
from app.exceptions.http_exceptions import BadRequestError
from app.repositories.seller_repository import SellerRepository

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
