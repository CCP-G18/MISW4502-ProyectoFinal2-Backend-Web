from unittest.mock import MagicMock, patch
from app.repositories.customer_repository import CustomerRepository
from app.models.customer_model import Customer

@patch("app.core.database.db.session")
def test_create_customer(mock_session):
    # Crear un cliente simulado
    mock_customer = Customer(
        identification_type="CC",
        identification_number=123456789,
        country="Colombia",
        city="Bogotá",
        address="Calle 123",
        user_id="4e49e816-e4b0-4d94-974b-8b35d905ae21"
    )

    result = CustomerRepository.create(mock_customer)

    # Verificar que se llamó a db.session.add() con el cliente
    mock_session.add.assert_called_once_with(mock_customer)

    # Verificar que se llamó a db.session.commit()
    mock_session.commit.assert_called_once()
 
    assert result == mock_customer