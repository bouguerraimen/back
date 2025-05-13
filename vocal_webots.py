import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="https://front-npmn.onrender.com/", async_mode='eventlet')

clients = []

@app.route('/')
def index():
    return jsonify({"message": "Serveur Flask SocketIO en ligne"})

@socketio.on('send_command')
def handle_command(data):
    command = data.get('command', '')
    print(f"✅ Commande reçue : {command}")
    for client in clients:
        socketio.emit('execute_command', {'command': command}, room=client)

@socketio.on('connect')
def handle_connect():
    clients.append(request.sid)
    print(f"🔌 Client connecté : {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in clients:
        clients.remove(request.sid)
    print(f"❌ Client déconnecté : {request.sid}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
