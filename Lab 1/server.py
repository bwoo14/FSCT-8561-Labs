import socket


# Set Variables for host IP and Port number
HOST = "127.0.0.1"
PORT = 12345

# Create socket
server_socket = socket.socket(
    socket.AF_INET, # Use IPv4
    socket.SOCK_STREAM # Use TCP
)

# Bind to specified host/port then listen
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Server is waiting for a connection...")

# Accept a client connection
client_socket, client_address = server_socket.accept()

print("Connected by:", client_address)

username = None
connected = True


# Maintain stateful connection using while loop
while connected:
    # Try/except clause to handle errors
    try:
        # receive data 
        data = client_socket.recv(1024)

        # handle client disconnection
        if not data:
            print("Client disconnected unexpectedly")
            break

        # Decode data
        message = data.decode()

        print("Received:", message)

        # Input Data Validation
        if "|" not in message:
            client_socket.send(
                "ERROR|Invalid command format".encode()
            )
            continue
        # Split data by delimeter "|"
        command, content = message.split("|", 1)

        # Handle cases for different commands
        if command == "HELLO": # case for "HELLO" command

            # Ensure User entered username
            if content == "":
                client_socket.send(
                    "ERROR|Username required".encode()
                )
            # Set Username to what content was
            else:
                username = content
                print("Username:", username)
                # Send message to client with command "OK" and confirmation that username accepted
                client_socket.send(
                    "OK|Hello ".encode() + username.encode()
                )

        elif command == "MSG": # case for "MSG" command

            # Ensure user has set their username
            if username is None:
                client_socket.send(
                    "ERROR|HELLO required first".encode()
                )
            # Ensure message is not empty
            elif content == "":
                client_socket.send(
                    "ERROR|Message cannot be empty".encode()
                )
            # Handle error for message too long (can't be more than 200 characters)
            elif len(content) > 200:
                client_socket.send(
                    "ERROR|Message too long".encode()
                )
            else:
                # print message
                print(username + " says:", content)

                # Confirm with client that message was received
                client_socket.send(
                    ("OK|Message received from " + username).encode()
                )

        elif command == "EXIT": # case for "EXIT" command

            # Confirm connection termination
            client_socket.send(
                "OK|Goodbye".encode()
            )
            
            # terminate connection (break loop)
            connected = False

        else: # Handle unknown commands
            client_socket.send(
                "ERROR|Unknown command".encode()
            )

    except ConnectionResetError:
        print("Connection reset by client")
        break

# Close socket and connection
client_socket.close()
server_socket.close()

print("Server closed")
