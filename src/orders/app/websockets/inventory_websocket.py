from flask import has_request_context, request
from flask_socketio import emit
from app.extensions import socketio


connected_sellers = {}

@socketio.on('connect')
def handle_connect():
    seller_id = request.args.get('seller_id')
    if seller_id:
        connected_sellers[seller_id] = request.sid
        print(f"Vendedor {seller_id} conectado.")

@socketio.on('disconnect')
def handle_disconnect():
    seller_id = None
    for key, value in connected_sellers.items():
        if value == request.sid:
            seller_id = key
            break
    if seller_id:
        del connected_sellers[seller_id]
        print(f"Vendedor {seller_id} desconectado.")

@socketio.on('update_inventory')
def notify_inventory_update(product_id, product_name, new_quantity):
    message = {
        "type": "inventory_update",
        "product": {
            "id": product_id,
            "name": product_name,
            "new_quantity": new_quantity
        } 
    }
    for sid in connected_sellers.values():
        try:
            socketio.emit('inventory_update', message, to=sid)
            print(f"Notificación enviada a vendedor {sid}: {message}")
        except Exception as e:
            if has_request_context():
                try:
                    socketio.emit('inventory_error', {
                        "error": "No se pudo enviar la notificación a uno o más vendedores.",
                        "product_id": product_id,
                        "product_name": product_name,
                    }, to=request.sid)
                except RuntimeError:
                    pass
            break