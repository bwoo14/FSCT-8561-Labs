import socket

# Create vairalbes for IP and Port number
HOST = "127.0.0.1"
PORT = 12345

# create socket 
client_socket = socket.socket(
    socket.AF_INET, # Use IPv4
    socket.SOCK_STREAM # Use TCP
)

# Connet to server using the host and the port
client_socket.connect((HOST, PORT))

message = "Hello Server"

# Send the message
client_socket.send(message.encode())


# save then print the response
response = client_socket.recv(1024)

print("Server replied:", response.decode())

# close connection
client_socket.close()