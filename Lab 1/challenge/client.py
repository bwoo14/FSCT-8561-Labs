import socket
import threading

# Code refactored from https://www.geeksforgeeks.org/python/socket-programming-multi-threading-python/

# Multi-threaded function to handle incoming messages
def receive_messages(s):
    while True:
        try:
            # Receive data
            data = s.recv(1024)
            if not data:
                print("\nServer disconnected.")
                break

            # Print data on new line
            print("\n", data.decode())

        except (ConnectionResetError, OSError):
            break

def main():
    # Set host and port
    host = '127.0.0.1'
    port = 12345

    # Set socket to use IPv4 and TCP and connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))


    # Send username to server
    username = input("Enter your username: ")
    msg = "HELLO|" + username
    s.send(msg.encode()) 

    # Setup a thread to receive messages from server
    receiver = threading.Thread(
        target=receive_messages,
        args=(s,),
        daemon=True
    )

    # Start the receiver
    receiver.start()


    # While loop for chat messages
    while True:
        # Get message from client
        msg = input("> ")
        if msg.upper() == "EXIT":
        
            # Sending "EXIT" command to server
            s.send(
                "EXIT|".encode()
            )
            # Tell client that they are diconnecting
            print("Disconnecting from server...")
            break

        # Send message to server for broadcast
        msg = "MSG|" + msg
        s.send(msg.encode())

    # Close connections
    s.close()
    receiver.join()
    print("Disconnected from Server")

if __name__ == '__main__':
    main()