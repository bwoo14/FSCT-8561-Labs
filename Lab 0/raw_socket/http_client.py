import socket

# Create socket and connect to example.com on port 80
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("example.com", 80))

# Format the request (HTTP GET request)
request = (
    "GET / HTTP/1.1\r\n"
    "Host: example.com\r\n"
    "Connection: close\r\n"
    "\r\n"
)

# send message after it is encoded
client.send(request.encode())

# get the response and break after the server is finished
response = b""
while True:
    data = client.recv(4096)
    if not data:
        break
    response += data

# print the response
print(response.decode(errors="replace"))

# close the connection
client.close()