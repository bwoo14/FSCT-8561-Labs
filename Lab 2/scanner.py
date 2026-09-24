import socket
import sys

# Create function to scan port
def scan_port(target, port):

	# Create socket
	scanner_socket = socket.socket(
		socket.AF_INET, # Use IPV4
		socket.SOCK_STREAM # Use TCP
	)

	# Set timeout to 0.5s
	scanner_socket.settimeout(0.5)

	# Scan socket and record error code
	result = scanner_socket.connect_ex(
		(target, port)
	)
	# Close socket
	scanner_socket.close()

	# Return true if port connected without error
	if result == 0:
		return True
	else:
		return False
	
	
def get_host_input(prompt):
	# Check if hostname is valid
	invalid = True
	while invalid:
		target = input(prompt)
		try:
			target_ip = socket.gethostbyname(target)
			print ("INFO - IP Resolved - Target IP is ", target_ip)
		except socket.gaierror:
			print("ERROR: Invalid hostname or IP address")
			continue
		break
	return target

# Get port input
def get_port_input(prompt, starting_port=0):
	invalid = True
	while invalid:
		# Make sure user entered an integer
		try:
			port = int(input(prompt))
		except:
			print("ERROR: Enter a valid integer between 1 and 65535")
			continue

		# Ensure that the end port is bigger than the starting port
		if port < starting_port:
			print("ERROR: End Port must be larger than Starting Port")
			continue

		# make sure port within correct range
		if not (1 <= port <= 65535):
			print("ERROR: Invalid Port Number - Port must be between 1 and 65535")
			continue
		
		if (starting_port != 0) and (port - starting_port > 1000):
			print("ERROR: Port Range too large. Try something smaller")
		else:
			return port




# Get inputs from user
target = get_host_input("Target host: ")
start_port = get_port_input("Start port: ")
end_port = get_port_input("End port: ", starting_port=start_port)

# Quit if range is too large
if end_port - start_port >= 1000:
	print("ERROR: Range too large")
	quit()

open_ports = []
print()
print("INFO - Port scan starting...")
# Scan through each port
for port in range(start_port, end_port + 1):
	print(f"INFO - Scanning port {port}...")
	# if port open, appened to open ports and print open port
	if scan_port(target, port):
		# See if we can get likely service
		try:
			service = socket.getservbyport(
				port,
				"tcp"
			)
		except OSError:
			service = "unknown"

		print(f"INFO - Port {port} is OPEN - Likely service: {service}")
		open_ports.append((port, service))
	else:
		print(f"INFO - Unsuccessful Connection to port {port}")

print()
# If open_ports less than 1, print no open ports. Else, print open ports
if len(open_ports) < 1:
	print("No open ports found in the selected range")
else:
	print(f"{'Port':<10} {'Service'}")
	print("-" * 25)
	for port, service in open_ports:
		print(f"{port:<10} {service}")
print()
print("Scan Complete.")

