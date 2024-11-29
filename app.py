# app.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Store messages in memory (replace with database in production)
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    message = {
        'id': str(uuid.uuid4()),
        'username': data['username'],
        'message': data['message']
    }
    messages.append(message)
    emit('receive_message', message, broadcast=True)

@app.route('/messages')
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    socketio.run(app, debug=True)