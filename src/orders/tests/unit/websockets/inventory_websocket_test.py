import pytest
from flask import Flask
from app.extensions import socketio
from app.websockets.inventory_websocket import connected_sellers, notify_inventory_update

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    socketio.init_app(app, cors_allowed_origins="*")
    return app

def test_connect_and_disconnect(app):
    client = socketio.test_client(app, query_string='seller_id=seller123')
    
    assert client.is_connected()
    assert 'seller123' in connected_sellers

    client.disconnect()
    assert 'seller123' not in connected_sellers

def test_inventory_update_emits_to_all(app, mocker):
    client1 = socketio.test_client(app, query_string='seller_id=1')
    client2 = socketio.test_client(app, query_string='seller_id=2')
    products = [
        {'product_id': 'e6291db2-0d4e-46b6-80a3-b85dc289d4c0', 'name': 'Avena', 'new_quantity': 5}, 
        {'product_id': 'e6291db2-0d4e-46b6-80a3-b85dc289d4c0', 'name': 'Avena', 'new_quantity': 4}
    ]

    emit_spy = mocker.spy(socketio, 'emit')
    
    notify_inventory_update(products)

    calls = [call for call in emit_spy.call_args_list if call[0][0] == 'inventory_update']
    assert len(calls) == 2

    client1.disconnect()
    client2.disconnect()

def test_emit_fails_and_sends_error(app, mocker):
    client = socketio.test_client(app, query_string='seller_id=error_test')
    products = [
        {'product_id': 'e6291db2-0d4e-46b6-80a3-b85dc289d4c0', 'name': 'Avena', 'new_quantity': 5}, 
        {'product_id': 'e6291db2-0d4e-46b6-80a3-b85dc289d4c0', 'name': 'Avena', 'new_quantity': 4}
    ]
    emit_original = socketio.emit

    def faulty_emit(event, data, to=None):
        if event == "inventory_update":
            raise Exception("Simulado")
        return emit_original(event, data, to=to)

    mocker.patch('app.extensions.socketio.emit', side_effect=faulty_emit)
    notify_inventory_update(products)

    client.disconnect()