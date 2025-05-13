from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins="https://front-npmn.onrender.com/")  

socketio = SocketIO(app, cors_allowed_origins="https://front-npmn.onrender.com/")

clients = []

@app.route('/')
def index():
    return jsonify({"message": "Serveur Flask SocketIO en ligne"})

@socketio.on('send_command')
def handle_command(data):
    command = data.get('command', '')
    print(f"Commande reçue du frontend : {command}")
    
    for client in clients:
        socketio.emit('execute_command', {'command': command}, room=client)
        print(f"Commande envoyée au robot : {command}")

@socketio.on('connect')
def handle_connect():
    clients.append(request.sid)
    print(f"Robot connecté : {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in clients:
        clients.remove(request.sid)
    print(f"Robot déconnecté : {request.sid}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
