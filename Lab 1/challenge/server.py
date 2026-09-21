import socket
import threading
from _thread import start_new_thread

# Code refactored from https://www.geeksforgeeks.org/python/socket-programming-multi-threading-python/

# Create empty dict for active clients
CLIENTS = {}

# Handle broadcasting messages across clients
def broadcast(message, username):

	# Format message to have username 
	message = f"{username}: {message}"

	# Loop over each client and send
	for client in CLIENTS.values():

		# If sender = client, don't forward. Stops the sender from receivint eh message
		if client["username"] == username:
			continue

		# Send message to client
		try:
			client["socket"].sendall(message.encode())
		except OSError:
			pass

# Handle new client connections using multithreading
def handle_client(c,):

	# Get port
	c_port = c.getpeername()[1]
	connected = True


	try:
		# Start while loop
		while connected:
			# receive data
			data = c.recv(1024)

			# break if no data sent
			if not data:
				print('DISCONNECTED')
				break
			message = data.decode() 

			# handle improper message format from clinet, don't crash, just restart while loop
			if "|" not in message:
				c.send("ERROR|Invalid command format".encode())
				continue

			# Split data by delimeter "|"
			command, content = message.split("|", 1)

			if command == "HELLO": # case for "HELLO" command
				# Ensure User entered username
				if content == "":
					c.send("ERROR|Username required".encode())
					# Set Username to what content was
				else:
					# Get username
					username = content
					print(f"INFO - {c_port} set username to: {username}")

					# Add username and connection to CLIENTS dict
					CLIENTS[c_port] = {"username": username, "socket": c}
					# Send message to client with command "OK" and confirmation that username accepted
					c.send(f"Connection Successful! Hello {username}".encode())

					# Debbugging, showing the connected clients
					print("=== INFO - Connected Clients: ===")
					for port, client in CLIENTS.items():
						print(f"Port: {port}, Username: {client['username']}")
					print("=================================")


			elif command == "EXIT": # case for "EXIT" command
				# Confirm connection termination
				c.send(
    	            "Successfully disconnected from the server".encode()
    	        )
    	        # terminate connection (break loop)
				connected = False

			elif command == "MSG": # case for "MSG" command
    	        # Ensure user has set their username
				if username is None:
					c.send(
    	                "ERROR|HELLO required first".encode()
    	            )
    	        # Ensure message is not empty
				elif content == "":
					c.send(
    	                "ERROR|Message cannot be empty".encode()
    	            )
    	        # Handle error for message too long (can't be more than 200 characters)
				elif len(content) > 200:
					c.send(
    	                "ERROR|Message too long".encode()
    	            )
				else:
    	            # debugging, log incoming message 
					print(f"=== INFO - Incoming message from: {username} ===")
					print(f"=== INFO - Broadcasting Message ===")

					# broadcast message to all clients
					broadcast(content, username)
			else: # Handle unknown commands
				c.send(
    	            "ERROR|Unknown command".encode()
    	        )
	except ConnectionResetError:
		print(f"=== INFO - {username} disconnected ===")
	finally:
		# Remove client from list
		CLIENTS.pop(c_port, None)
		# Close connection
		c.close()
		# Debugging, log that connection was closed
		print(f"=== INFO - Connection closed on: {c_port} ===")

def main():
	# Create socket
	s = socket.socket(
		socket.AF_INET, # Use IPv4
	    socket.SOCK_STREAM # Use TCP
	)
	# set port number and host address
	HOST = "127.0.0.1"
	PORT = 12345

	# Bind then listen 
	s.bind((HOST, PORT))
	s.listen()

	# Debugging, tell what port server is on
	print("=== Server running on port: ", PORT, " ===")

	try:
		# Start while loop to accept incoming connections
		while True:
			# Accept connection
			c, addr = s.accept()

			# Debugging, log connection and port number
			print('Connected to:', addr[0], ':', addr[1])

			# Start thread to handle multiple clients
			threading.Thread(target=handle_client, args=(c,), daemon=True).start()

			
	except KeyboardInterrupt:
		print("Closing Connections")
	finally:
		# Close connection
		s.close()



if __name__ == '__main__':
	main()