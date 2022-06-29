import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("Connected")

@sio.event
def connect_error():
    print('[INFO] Failed to connect to server.')

@sio.event
def disconnect():
    print('[INFO] Disconnected from server.')


@sio.on("message")
def message_received(message):
    print(message)


sio.connect('http://localhost:3000')

sio.emit("something", "Hello from python.")