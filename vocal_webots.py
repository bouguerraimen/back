from flask import Flask, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

clients = []

# ✅ Route HTTP classique pour tester que le backend est actif
@app.route('/')
def index():
    return jsonify({"message": "Serveur Flask SocketIO en ligne"})

# Reçoit les commandes du frontend
@socketio.on('send_command')
def handle_command(data):
    command = data.get('command', '')
    print(f"Commande reçue du frontend : {command}")
    
    # Envoie la commande à tous les robots connectés
    for client in clients:
        socketio.emit('execute_command', {'command': command}, room=client)
        print(f"Commande envoyée au robot : {command}")

# Gestion des connexions robots
@socketio.on('connect')
def handle_connect():
    clients.append(request.sid)
    print(f"Robot connecté : {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    clients.remove(request.sid)
    print(f"Robot déconnecté : {request.sid}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)


# Gestion des connexions robots
@socketio.on('connect')
def handle_connect():
    clients.append(request.sid)
    print(f"Robot connecté : {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    clients.remove(request.sid)
    print(f"Robot déconnecté : {request.sid}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
