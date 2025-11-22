from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import os
from threading import Lock

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)
PORT = 8000
ready_for_question = True
thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(5)
        count += 1
        socketio.emit('counter_update', {'count': count})

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/reset', methods=['POST'])
def reset():
    global ready_for_question
    ready_for_question = True
    print("Reset: Ready for question")
    socketio.emit('reset_state')
    return "OK", 200

@socketio.on('connect')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    print('Client connected')
    emit('my response', {'data': 'Connected'})

if __name__ == '__main__':
    print(f"Serving HTTP on port {PORT} ...")
    print(f"Open http://localhost:{PORT} in your browser")
    socketio.run(app, port=PORT, debug=True)
