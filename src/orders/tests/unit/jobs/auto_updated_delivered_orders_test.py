from unittest.mock import patch, MagicMock, ANY
from datetime import datetime
from flask import Flask
from app.jobs.auto_update_delivered_orders import auto_update_delivered_orders
from app.models.order_model import OrderStateEnum

@patch("app.jobs.auto_update_delivered_orders.db")
@patch("app.jobs.auto_update_delivered_orders.datetime")
def test_auto_update_delivered_orders_updates_orders(mock_datetime, mock_db):
    # Simular datetime.utcnow().date() → 2025-05-17
    fake_now = datetime(2025, 5, 17, 15, 30, 0)
    mock_datetime.utcnow.return_value = fake_now
    mock_datetime.combine.side_effect = datetime.combine
    mock_datetime.date = datetime.date
    mock_datetime.time = datetime.time

    # Simular query
    mock_session = mock_db.session
    mock_session.query.return_value.filter.return_value.update.return_value = 3

    # Crear app Flask mínima para el contexto
    app = Flask(__name__)
    with app.app_context():
        auto_update_delivered_orders(app)

    # Validaciones
    mock_session.query.assert_called_once()
    mock_session.query.return_value.filter.assert_called_once()
    mock_session.query.return_value.filter.return_value.update.assert_called_once_with(
        ANY, synchronize_session=False
    )
    mock_session.commit.assert_called_once()
