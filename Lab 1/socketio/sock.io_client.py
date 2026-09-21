import socketio

# Code taken and adjusted from "Mastering Python for Networking and Security"

# Initiate client
sio = socketio.Client()

# Handle Connect event
@sio.event
def connect():
	print("connection established")

# Handle responses from the server and print them
@sio.event
def response(data):
	print(data)

# Connect to the server
sio.connect("http://localhost:8080")

# Set username and send to server
message = input("What is your username: ")
sio.emit("hello", message)

# start chat function using while loop
while True:
	# Get input from client
	message = input("Enter your message: ")

	# If client types EXIT, disconnect from server
	if message == "EXIT":
		print("Disconnecting")
		sio.emit('disconnect')
		break

	# Send message
	sio.emit('chat', message)
		


	
