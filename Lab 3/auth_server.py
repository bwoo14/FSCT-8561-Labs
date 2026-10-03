import socket
import pyotp
import hashlib

# logging function
def logging(type, message):
	print(f"{type} - {message}")

# Function that hashes passwords using SHA256
def hash_password(password):
	return hashlib.sha256(
		password.encode()
	).hexdigest()


# return true if password correct, otherwise false
def verify_password(entered_hash, stored_hash):
	if entered_hash == stored_hash:
		return True
	else:
		return False
# Return true if OTP matches, otherwise False
def verify_otp(secret, otp):
	totp = pyotp.TOTP(secret)
	return totp.verify(otp)

# Users Dictionary
brandon_secret = pyotp.random_base32()
USERS = {
	"brandon": {
		"password_hash": hash_password("brandon"),
		"totp_secret": brandon_secret,
		"password_verified": False,
		"authenticated": False
	}
}

# Set Variables for host IP and Port number
HOST = "127.0.0.1"
PORT = 12345

# Create socket
server_socket = socket.socket(
	socket.AF_INET,		# Use IPv4
	socket.SOCK_STREAM	# Use TCP
)

# Bind to specified host/port then listen
server_socket.bind((HOST, PORT))
server_socket.listen(1)

logging("INFO", "Server is waiting for a connection...")

# Accept a client connection
client_socket, client_address = server_socket.accept()
# client_socket.send("OK|Connection to Server Successful".encode())
logging("INFO", f"Connected by: {client_address}")


connected = True

# Set Empty username to prevent empty variable errors
username=""

# Set Login attempts to 0
login_attempts = 0
# Maintain stateful connection using while loop
while connected:
	# If login attempts is greater than or equal to 3, stop accepting requests
	if login_attempts >= 3:
		logging("ERROR", f"Too many failed attempts. Authentication blocked for {client_address}")
		client_socket.send("AUTH_ERROR|ACCESS DENIED - Too many failed attempts. Authentication blocked.".encode())
		data = client_socket.recv(1024)
	else:
		# Try/except clause to handle errors
		try:
			# Receive data
			data = client_socket.recv(1024)

			# Handle client disconnection
			if not data:
				logging("INFO", f"Client {client_address} disconnected unexpectedly")
				break

			# Decode data
			message = data.decode()

			logging("INFO", f"Received -- {message} -- from {client_address}")

			# Input Data Validation
			if "|" not in message:
				client_socket.send(
					"ERROR|Invalid command format".encode()
				)
				continue

			# Split data by delimiter "|"
			command, content = message.split("|", 1)

			# Handle cases for different commands
			if command == "AUTH":
				# Ensure user entered username
				if content == "":
					client_socket.send(
						"ERROR|Authentication Failed".encode()
					)

				# Set Username and password to what content was
				else:
					try:
						username, password = content.split("|", 1)
					except ValueError:
						logging("ERROR", f"Malformed authentication message from {client_address}")
						client_socket.send("ERROR|Malformed Message - Authentication Failed".encode())
						continue
					print("Authenticating:", username)

					# Verify if username exists, otherwise advise client
					try:
						user = USERS[username]
					except KeyError:
						logging("INFO", f"Failed username from {client_address}")
						client_socket.send(
							"AUTH_ERROR|User does not exist".encode()
						)
						continue
					# Verify if password is correct
					if not verify_password(hash_password(password), USERS[username]["password_hash"]):
						logging("INFO", f"Incorrect password from {client_address} for username: {username}")
						# Advise client password was incorrect
						client_socket.send(
							"AUTH_ERROR|Incorrect Password".encode()
						)

						# Increase login attempt by 1
						login_attempts += 1
						logging("INFO", f"{client_address} login attempts remaining: {3 - login_attempts}")
					else:
						client_socket.send(
							"OK|OTP_REQUIRED - Please input TOTP".encode()
						)
						# Set password verified to true so we can ask for OTP
						USERS[username]["password_verified"] = True

			elif command == "OTP":
				otp = content
				try:
					# Confirm user is password verified before asking for OTP
					if USERS[username]["password_verified"]:
						if verify_otp(USERS[username]["totp_secret"], otp):
							# if OTP verified, authenticate user 
							USERS[username]["authenticated"] = True
							logging(f"INFO", f"Successful login for {username}")
							client_socket.send(f"OK|ACCESS GRANTED".encode())

							# Reset login count to 0
							login_attempts = 0
						else:
							logging("INFO", f"Incorrect OTP Code from {username} on {client_address}")
							client_socket.send(f"ERROR|ACCESS DENIED - Incorrect OTP".encode())
							# Increase failed login for 
							login_attempts += 1
							logging("INFO", f"{client_address} login attempts remaining: {3 - login_attempts}")
					else:
						# If user not password verified, tell user to sign in with username and password first
						logging("INFO", f"{client_address} tried signing in without username and password first")
						client_socket.send(f"ERROR|You must sign in with username and password before entering your OTP".encode())
				except KeyError:
					logging("INFO", f"{client_address} tried signing in without username and password first")
					client_socket.send(f"ERROR|You must sign in with username and password before entering your OTP".encode())

			elif command == "MSG":
				# Ensure user has set their username
				if not USERS[username]["authenticated"]:
					client_socket.send(
						"ERROR|Authentication required first".encode()
					)

				# Ensure message is not empty
				elif content == "":
					client_socket.send(
						"ERROR|Message cannot be empty".encode()
					)

				# Handle error for message too long
				# (can't be more than 200 characters)
				elif len(content) > 200:
					client_socket.send(
						"ERROR|Message too long".encode()
					)

				else:
					# Print message
					logging("INFO", f"{username} says: {content}")

					# Confirm with client that message was received
					client_socket.send(
						("OK|Message received from " + username).encode()
					)

			elif command == "EXIT":

				# Confirm connection termination
				client_socket.send(
					"OK|Goodbye".encode()
				)

				# Terminate connection
				USERS["brandon"]["authenticated"] = False
				USERS["brandon"]["password_verified"] = False
				connected = False

			else:

				# Handle unknown commands
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


