import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from app.services.product_service import ProductService, BadRequestError
from app.models.product_model import Product
import io
import pandas as pd
import uuid

valid_product_data = {
  "name": "Test Product",
  "description": "A test description",
  "unit_amount": 100.0,
  "quantity": 5,
  "image_url": "http://example.com/image.jpg",
  "manufacturer_id": "123e4567-e89b-12d3-a456-426614174000",
  "category_id": "123e4567-e89b-12d3-a456-426614174001"
}

@pytest.fixture
def mock_product():
  return valid_product_data

@pytest.fixture
def mock_products(mock_product):
  return [mock_product]

@pytest.fixture
def app():
  app = Flask(__name__)
  app.config['TESTING'] = True
  return app
  
@pytest.fixture
def client(app):
  return app.test_client()

def test_create_success():
  with patch("app.services.product_service.ProductRepository.create") as mock_create:
    mock_create.return_value = MagicMock()

    result = ProductService.create(valid_product_data)

    mock_create.assert_called_once()
    assert result == mock_create.return_value

@pytest.mark.parametrize("field, expected_msg", [
  ("name",            "El nombre es requerido"),
  ("description",     "La descripción es requerida"),
  ("unit_amount",     "El monto es requerido"),
  ("quantity",        "La cantidad es requerida"),
  ("image_url",        "La url de la imagen es requerida"),
  ("manufacturer_id", "El fabricante es requerido"),
  ("category_id",     "La categoría es requerida"),
])
def test_create_product_missing_required_field(field, expected_msg):
  data = valid_product_data.copy()
  data.pop(field, None)

  with pytest.raises(BadRequestError, match=expected_msg):
    ProductService.create(data)
      
def test_create_invalid_manufacturer_id():
  data = valid_product_data.copy()
  data["manufacturer_id"] = "invalid-uuid"

  with pytest.raises(BadRequestError) as excinfo:
    ProductService.create(data)

  assert "fabricante no es válido" in str(excinfo.value).lower()

def test_create_invalid_category_id():
  data = valid_product_data.copy()
  data["category_id"] = "invalid-uuid"

  with pytest.raises(BadRequestError) as excinfo:
    ProductService.create(data)

  assert "categoría no es válida" in str(excinfo.value).lower()

@patch('app.repositories.product_repository.ProductRepository.get_all')
def test_get_all_success(mock_get_all):
    prod1 = MagicMock(id="prod-1111")
    prod2 = MagicMock(id="prod-2222")
    mock_get_all.return_value = [prod1, prod2]

    result = ProductService.get_all()

    mock_get_all.assert_called_once()
    assert result == [prod1, prod2]

@patch('app.repositories.product_repository.ProductRepository.get_product_by_id')
def test_get_product_by_id_success(mock_get_product_by_id):
    product_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_product = MagicMock(id=product_id, name="Test Product")
    mock_get_product_by_id.return_value = mock_product

    result = ProductService.get_product_by_id(product_id)
    mock_get_product_by_id.assert_called_once_with(product_id)
    assert result == mock_product

def test_get_product_by_id_invalid_id():
    invalid_product_id = "invalid-uuid"

    with pytest.raises(BadRequestError, match="El id no es válido"):
        ProductService.get_product_by_id(invalid_product_id)

@patch('app.repositories.product_repository.ProductRepository.get_product_by_id')
def test_get_product_by_id_not_found(mock_get_product_by_id):    
    product_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_get_product_by_id.return_value = None

    with pytest.raises(BadRequestError, match="El producto no existe"):
        ProductService.get_product_by_id(product_id)
    mock_get_product_by_id.assert_called_once_with(product_id)

@patch('app.repositories.product_repository.ProductRepository.get_product_by_id')
@patch('app.repositories.product_repository.ProductRepository.update')
def test_update_quantity_success(mock_update, mock_get_product_by_id):
    product_id = "123e4567-e89b-12d3-a456-426614174000"
    product_data = {"quantity": 10}
    mock_product = MagicMock(id=product_id, quantity=5)
    mock_get_product_by_id.return_value = mock_product
    mock_update.return_value = mock_product

    result = ProductService.update_quantity(product_id, product_data)

    mock_get_product_by_id.assert_called_once_with(product_id)
    mock_update.assert_called_once_with(mock_product)
    assert result.quantity == product_data["quantity"]

def test_update_quantity_invalid_id():
    invalid_product_id = "invalid-uuid"
    product_data = {"quantity": 10}

    with pytest.raises(BadRequestError, match="El ID del producto no es válido"):
        ProductService.update_quantity(invalid_product_id, product_data)

def test_update_quantity_missing_quantity():
    product_id = "123e4567-e89b-12d3-a456-426614174000"
    product_data = {}

    with pytest.raises(BadRequestError, match="La cantidad es requerida"):
        ProductService.update_quantity(product_id, product_data)

def test_update_quantity_invalid_quantity():    
    product_id = "123e4567-e89b-12d3-a456-426614174000"
    invalid_quantities = [-1, "invalid"]
    for invalid_quantity in invalid_quantities:
        product_data = {"quantity": invalid_quantity}

        with pytest.raises(BadRequestError, match="La cantidad debe ser un número entero no negativo"):
            ProductService.update_quantity(product_id, product_data)

@patch('app.repositories.product_repository.ProductRepository.get_product_by_id')
def test_update_quantity_product_not_found(mock_get_product_by_id):
    product_id = "123e4567-e89b-12d3-a456-426614174000"
    product_data = {"quantity": 10}
    mock_get_product_by_id.return_value = None

    with pytest.raises(BadRequestError, match="El producto no existe"):
        ProductService.update_quantity(product_id, product_data)
    mock_get_product_by_id.assert_called_once_with(product_id)

@patch('app.repositories.product_repository.ProductRepository.get_products_by_category')
def test_get_products_by_category_success(mock_get_products_by_category):
    category_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_products = [MagicMock(id="prod-1111"), MagicMock(id="prod-2222")]
    mock_get_products_by_category.return_value = mock_products

    result = ProductService.get_products_by_category(category_id)

    mock_get_products_by_category.assert_called_once_with(category_id)
    assert result == mock_products

def test_get_products_by_category_invalid_id():
    invalid_category_id = "invalid-uuid"

    with pytest.raises(BadRequestError, match="El id de la categoría no es válido"):
        ProductService.get_products_by_category(invalid_category_id)

@patch('app.repositories.product_repository.ProductRepository.get_products_by_category')
def test_get_products_by_category_not_found(mock_get_products_by_category):
    category_id = "123e4567-e89b-12d3-a456-426614174000"
    mock_get_products_by_category.return_value = []

    with pytest.raises(BadRequestError, match="No hay productos en esta categoría"):
        ProductService.get_products_by_category(category_id)

    mock_get_products_by_category.assert_called_once_with(category_id)

def test_parse_and_validate_file_csv():
  df = pd.DataFrame([
    {
      "Nombre del producto": "Producto de prueba",
      "Descripción": "Un producto válido",
      "Cantidad inicial": 50,
      "Precio unitario": 12000,
      "Nombre del fabricante": "fabricante test masivo",
      "Nombre de la categoría": "categoría test masiva"
    },
    {
      "Nombre del producto": "",
      "Descripción": "Sin nombre",
      "Cantidad inicial": 100,
      "Precio unitario": 8000,
      "Nombre del fabricante": "fabricante test masivo",
      "Nombre de la categoría": "categoría test masiva"
    }
  ])

  csv_buffer = io.StringIO()
  df.to_csv(csv_buffer, index=False)
  csv_buffer.seek(0)
  csv_buffer.filename = "archivo_prueba.csv"

  mock_manufacturer = MagicMock()
  mock_manufacturer.name = "Fabricante Test Masivo"
  mock_manufacturer.id = uuid.UUID("11111111-1111-1111-1111-111111111111")

  mock_category = MagicMock()
  mock_category.name = "Categoría Test Masiva"
  mock_category.id = uuid.UUID("22222222-2222-2222-2222-222222222222")

  with patch("app.services.product_service.Manufacturer") as mock_m_cls, \
      patch("app.services.product_service.Category") as mock_c_cls:

    mock_m_cls.query.all.return_value = [mock_manufacturer]
    mock_c_cls.query.all.return_value = [mock_category]

    result = ProductService.parse_and_validate_file(csv_buffer)

  assert result["cantidad_validos"] == 1
  assert result["cantidad_errores"] == 1
  assert result["errores"][0]["Nombre del producto"] == ""
  assert "Columna 'Nombre del producto' vacía" in result["errores"][0]["errores"]

def test_bulk_save_products_creates_and_saves():
  product_input = [
    {
      "name": "Producto Test",
      "quantity": 100,
      "category_id": uuid.uuid4(),
      "description": "Ejemplo",
      "manufacturer_id": uuid.uuid4(),
        "amount_unit": 12000
    }
  ]

  with patch("app.services.product_service.ProductRepository.save_bulk_products") as mock_save:
    result = ProductService.bulk_save_products(product_input)

    mock_save.assert_called_once()

    productos_pasados = mock_save.call_args[0][0]
    assert isinstance(productos_pasados, list)
    assert all(isinstance(p, Product) for p in productos_pasados)

    assert productos_pasados[0].name == "Producto Test"
    assert productos_pasados[0].quantity == 100
    assert productos_pasados[0].description == "Ejemplo"
    assert productos_pasados[0].unit_amount == 12000