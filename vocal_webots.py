from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import os

app = Flask(__name__)

# Autorise toutes les origines pendant les tests (ou remplace * par l'URL exacte du front)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="https://front-npmn.onrender.com/")

# Liste des clients connectés (robots ou autres)
clients = []

@app.route('/')
def index():
    return jsonify({"message": "Serveur Flask SocketIO en ligne"})

# Lorsqu'une commande est envoyée depuis le frontend
@socketio.on('send_command')
def handle_command(data):
    command = data.get('command', '')
    print(f"✅ Commande reçue du frontend : {command}")
    
    for client in clients:
        socketio.emit('execute_command', {'command': command}, room=client)
        print(f"➡️ Commande envoyée au client : {command}")

# Lorsqu'un client (robot) se connecte
@socketio.on('connect')
def handle_connect():
    clients.append(request.sid)
    print(f"🔌 Client connecté : {request.sid}")

# Lorsqu'un client se déconnecte
@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in clients:
        clients.remove(request.sid)
    print(f"❌ Client déconnecté : {request.sid}")

# Lancement de l'application sur le port fourni par Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
