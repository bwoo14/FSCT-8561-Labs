from aiohttp import web
import socketio

# Code taken and adjusted from "Mastering Python for Networking and Security"

# Create async server
socket_io = socketio.AsyncServer()

# Create web app to connect to
app = web.Application()

# attach it to the socket
socket_io.attach(app)

# used to initialize server
async def index(request):
	return web.Response(text='Helloworld from socketio',content_type='text/html')

# Handle disconnect event
@socket_io.on('disconnect')
async def disconnect(socket_id):
	print("Disconnecting: ", socket_id)
	# Disconnect socket 
	await socket_io.disconnect(socket_id)

# Handle chat events
@socket_io.on('chat')
async def print_chat(socket_id, data):
	# Print chat events with socket ID
	print(f"Message from {socket_id}: {data}")

# Handle login events, confirm if successful
@socket_io.on('hello')
async def print_message(socket_id, data):
	print("Connection by ", data)
	await socket_io.emit("response", "CONNECTION SUCCESSFUL -- Welcome: " + data)

# Needed for app to run
app.router.add_get('/', index)

# Start app
if __name__ == "__main__":
	web.run_app(app)