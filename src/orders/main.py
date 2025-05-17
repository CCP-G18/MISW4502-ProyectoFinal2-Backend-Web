from app import create_app
from app.extensions import socketio
import app.websockets.inventory_websocket

app = create_app()

if __name__ == "__main__":
    socketio.run(app)