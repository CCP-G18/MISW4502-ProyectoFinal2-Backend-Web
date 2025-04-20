import pytest
from unittest.mock import patch, MagicMock
from app.services.product_service import ProductService, BadRequestError
from app.repositories.product_repository import Product

valid_product_data = {
  "name": "Test Product",
  "description": "A test description",
  "unit_amount": 100.0,
  "quantity": 5,
  "manufacturer_id": "123e4567-e89b-12d3-a456-426614174000",
  "category_id": "123e4567-e89b-12d3-a456-426614174001"
}

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
