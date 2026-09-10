import socketio

# Create socket for client
sio = socketio.Client()

# Create connection event and send a message
@sio.event
def connect():
    print('connection established')
    sio.emit("my_message", {'hello': "HELLO SERVER ~ BRANDON WOO"})

# Create event for my_message, sends response to server
@sio.event
def my_message(data):
    print("INFO - Incoming Message :  ", data)
    print("INFO - Sending Reply...")
    sio.emit('my_response', {'response': 'I AM RESPONDING!! ~ BRANDON WOO'})

# Disconnect from server event
@sio.event
def disconnect():
    print('disconnected from server')

# Begin connection to server on port 5000
sio.connect('http://localhost:5000')
sio.wait()