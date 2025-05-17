import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("✅ Conectado al servidor como vendedor de prueba")

# Cuando se desconecta
@sio.event
def disconnect():
    print("❌ Desconectado del servidor")

# Cuando recibe una notificación
@sio.on('inventory_update')
def on_inventory_update(data):
    print(f"📦 Notificación recibida: {data}")

# Conexión al servidor Flask Socket.IO
sio.connect('http://localhost:5004?seller_id=123')
sio.wait()