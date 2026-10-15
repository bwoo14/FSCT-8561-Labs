import requests
import csv
BASE_URL = "http://localhost:3000"
SEARCH_URL = BASE_URL + "/rest/products/search"

TIMEOUT = 5

# Records should look like the following
# {
# 		"endpoint": "/",
# 		"http_method": "GET",
# 		"input/payload": "apple",
# 		"status code": "200",
# 		"response_length": 234
# }


# Format request summary to save for later
def format_request_summary(response, type, payload=None):
	
	response_summary = {
						"endpoint": response.url.replace(BASE_URL, ""),
						"http_method": type,
						"payload": payload,
						"status_code": response.status_code,
						"response_length": len(response.content),
						"content_type": response.headers.get("Content-Type"),
						"server_header": response.headers.get("Server")
					}
	# Print response headers
	for key in response_summary:
		print(f"{key}: {response_summary[key]}")
	return response_summary

def send_request(type, url, parameters=None, data=None):
	# Function to send requests, takes in url, method, and payload/data
	try:
		if type =="GET": # sending get requests
			response = requests.get(url, parameters,timeout=TIMEOUT)

			success_string = f"==== INFO: Connected to {BASE_URL} - {response.status_code} ===="
			print(success_string)
			response_summary = format_request_summary(response, type, payload=parameters)
			print("=" * len(success_string))

		elif type == "POST": # Sending post requests
			response = requests.post(url, data, timeout=TIMEOUT)
			success_string = f"==== INFO: Connected to {BASE_URL} - {response.status_code} ===="
			print(success_string)
			response_summary = format_request_summary(response, type, payload=data)
			print("=" * len(success_string))
		return response_summary
	except requests.RequestException as error:
		# handling errors
		print(f"ERROR: Could not connect to {url}:", error)
		return 0
		
# Function to handle to csv
def to_csv(records):
	with open("records.csv", "w", newline="", encoding="utf-8") as file:
		writer = csv.DictWriter(file, fieldnames=["endpoint", 
		                                          "status_code",
												  "http_method",
												  "content_type",
												  "response_length",
												  "payload",
												  "server_header"])
		writer.writeheader()
		writer.writerows(records)
	print("Saved records.csv")
		
records = []
# Testing GET / 
response_summary = send_request("GET", BASE_URL)
if response_summary:
	records.append(response_summary)

# Testing GET on /rest/products/search
for term in ["apple", "banana"]:
	response_summary = send_request("GET", SEARCH_URL, parameters={"q": term})
	if response_summary:
		records.append(response_summary)

# Sending post request
response_summary = send_request("POST", SEARCH_URL, data={"q": "apple"})
if response_summary:
	records.append(response_summary)

# Sending purposefully misformed request
response_summary = send_request("GET",  "http://localhost:300")
if response_summary:
	records.append(response_summary)

# Record csv
to_csv(records)