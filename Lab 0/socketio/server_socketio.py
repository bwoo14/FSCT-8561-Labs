import eventlet
import socketio

# Create server socket
sio = socketio.Server()

# Create web server, not used in this program much, but was in the original code
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

# Handle connection events
@sio.event
def connect(sid, environ):
    print('connect ', sid)

# Handle my_message events, prints request and sends response
@sio.event
def my_message(sid, data):
    print('message ', data)
    print("INFO - Sending Reply...")

	# Send Message to Client
    sio.emit('my_message', {
        'my_response': "HELLO CLIENT ~ BRANDON WOO"
	}, to=sid)

# Handle "my_reponse" events
@sio.event
def my_response(sid, data):
    print('Response from Client: ', data)

# Handle disconnection event
@sio.event
def disconnect(sid):
    print('disconnect ', sid)

# Start program and listen on port 5000
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)