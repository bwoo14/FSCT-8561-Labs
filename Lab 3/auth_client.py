import socket
from getpass import getpass


# Set host and port
HOST = "127.0.0.1"
PORT = 12345


# Create socket
client_socket = socket.socket(
	socket.AF_INET,		# Use IPv4
	socket.SOCK_STREAM	# Use TCP
)

# Connect to remote server
client_socket.connect((HOST, PORT))

password_authenticated = False

while not password_authenticated:

	# DEMO VALUE
	# value = input("DEMO VALUE: ")

	## DEMO: Malformed Message
	# auth_message = f"AUTH|{value}"

	# DEMO: OTP Before Password Verification
	# auth_message = f"OTP|{value}"

	# Prompt user to input their username
	username = input("Enter your username: ")
	password = getpass("Password: ")

	# Create string with command ("HELLO") and desired username
	auth_message = f"AUTH|{username}|{password}"



	# Send "AUTH" command to initiate username
	client_socket.send(
		auth_message.encode()
	)

	# Receive response
	response = client_socket.recv(1024)

	# Decode and print the response from the server
	print("Server:", response.decode())

	if "OTP_REQUIRED" in response.decode():
		password_authenticated = True

otp_authenticated = False
while not otp_authenticated:
	# Prompt user for TOTP Code
	otp = input("Enter your TOTP Code: ")

	# Format auth mesage
	otp_message = f"OTP|{otp}"

	# Send "AUTH" command to initiate username
	client_socket.send(
		otp_message.encode()
	)
		# Receive response
	response = client_socket.recv(1024)

	# Decode and print the response from the server
	print("Server:", response.decode())
	if not ("ACCESS DENIED" in response.decode()):
			otp_authenticated = True

# While loop to maintain connection to server
while True:

	# Prompt user for message to send
	message = input(
		"Enter message or type EXIT to leave: "
	)

	# Check if message is "EXIT"; if yes, terminate connection
	if message.upper() == "EXIT":

		# Sending "EXIT" command to server
		client_socket.send(
			"EXIT|".encode()
		)

		# Get server response, decode, and print
		response = client_socket.recv(1024)
		print("Server:", response.decode())

		# Break loop
		break

	# Format message to contain command
	protocol_message = "MSG|" + message

	# Send command to server
	client_socket.send(
		protocol_message.encode()
	)

	# Receive response, decode, and print
	response = client_socket.recv(1024)
	print("Server:", response.decode())


# Close connection
client_socket.close()

print("Disconnected")
