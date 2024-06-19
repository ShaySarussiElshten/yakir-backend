from flask import Flask, send_from_directory, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from datetime import datetime
from utils.cleanup import start_cleanup_thread, notifications

app = Flask(__name__, static_folder='../frontend/build')
CORS(app, resources={r"/api/*": {"origins": "*"}})


socketio = SocketIO(app, message_queue='redis://redis:6379/0', cors_allowed_origins="*")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    notifications_list = [{'msg': msg, 'time': time.isoformat()} for msg, time in list(notifications.queue)]
    return jsonify(notifications_list)


@socketio.on('send_notification')
def handle_notification(data):
    current_time = datetime.now()
    notification = (data['msg'], current_time)
    notifications.put(notification)
    socketio.emit('receive_notification', {'msg': data['msg'], 'time': current_time.isoformat()})


start_cleanup_thread()

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
