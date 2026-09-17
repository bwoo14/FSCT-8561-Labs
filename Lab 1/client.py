import socket

# Set host and port
HOST = "127.0.0.1"
PORT = 12345


# Create socket
client_socket = socket.socket(
    socket.AF_INET, # Use IPv4
    socket.SOCK_STREAM # use TCP
)

# Connect to remote server
client_socket.connect((HOST, PORT))

# Prompt user to input their username
username = input("Enter your username: ")

# Create string with command ("HELLO") and desired username
hello_message = "HELLO|" + username

# Send "HELLO" command to initiate username
client_socket.send(
    hello_message.encode()
)

# Receive response
response = client_socket.recv(1024)

# Decode and print the response from the server
print("Server:", response.decode())


# While loop to maintain connection to server
while True:

    # Prompt user for message to send
    message = input(
        "Enter message or type EXIT to leave: "
    )

    # Check if message is "EXIT"; if yes, teriminate conenction
    if message.upper() == "EXIT":

        # Sending "EXIT" command to server
        client_socket.send(
            "EXIT|".encode()
        )

        # Get server response, decode, and print
        response = client_socket.recv(1024)
        print("Server:", response.decode())

        # break loop
        break

    # format message to contain command
    protocol_message = "MSG|" + message
    

    # send command to server
    client_socket.send(
        protocol_message.encode()
    )

    # receive response, decode, and print
    response = client_socket.recv(1024)
    print("Server:", response.decode())

# Close connection
client_socket.close()

print("Disconnected")
