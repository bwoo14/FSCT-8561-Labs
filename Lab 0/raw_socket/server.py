import socket

# Specify host IP and port
HOST = "127.0.0.1"
PORT = 12345

# Create the server socket
server_socket = socket.socket(
    socket.AF_INET, # use IPv4
    socket.SOCK_STREAM # use TCP
)

# bind the socket to the host and port variables, start listening
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Server is waiting for a connection...")

# Get socket and client address when connection is made
client_socket, client_address = server_socket.accept()

# Print the clients address
print("Connected by:", client_address)

# Save the request
data = client_socket.recv(1024)

# Decode the message from bytes to plaintext
message = data.decode()

# print the message
print("Client says:", message)

# Create reply and send
reply = "Server Received"
client_socket.send(reply.encode())

# Close the socket
client_socket.close()
server_socket.close()
