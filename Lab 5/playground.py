import requests

# Set URL Variable
base_url = "http://localhost:3000"

# Send Get request
response = requests.get(base_url, timeout=5)

search_url = base_url + "/rest/products/search"

marker = "<u>fsct8561-test</u>"
marker_response = requests.get(search_url, params={"q": marker}, timeout=5)
print(marker_response.text)
if marker in marker_response.text:
	print("Marker appears in the response — investigate its context")
else:
	print("Marker was not found in this response")


normal_input = "apple"
probe_input = "'"
normal = requests.get(search_url, params={"q": normal_input},timeout=5)
probe = requests.get(search_url, params={"q": probe_input}, timeout=5)
print("Normal input status:", normal.status_code)
print("Probe input status:", probe.status_code)


error_phrase = "SQLITE_ERROR"
if error_phrase.lower() in probe.text.lower():
	print("Database-related error text found; manual review required")
else:
	print("No matching database error text in this response")


headers_to_check = ["Content-Security-Policy", "X-Content-Type-Options"]
for name in headers_to_check:
	if name in response.headers:
		print(name, "is present")
	else:
		print(name, "is not present; investigate its relevance")

print(response.headers.get("Server"))


alerts = []
seen = set()
for message in ["Missing CSP", "Missing CSP", "Missing X-Content-Type-Options"]:
	if message not in seen:
		seen.add(message)
		alerts.append(message)
print(alerts)

import csv
practice_records = [
	{"endpoint": "/", "status": 200},
	{"endpoint": "/example", "status": 404}
]
with open("practice_records.csv", "w", newline="", encoding="utf-8") as file:
	writer = csv.DictWriter(file, fieldnames=["endpoint", "status"])
	writer.writeheader()
	writer.writerows(practice_records)
print("Saved practice_records.csv")

# # Print status and length
# print("HTTP status:", response.status_code)
# print("Response length:", len(response.content), "bytes")

# # Print headers
# print("Content type:", response.headers.get("Content-Type"))
# print("First 100 characters:", response.text[:50])

# # Create search URL
# search_url = base_url + "/rest/products/search"
# # Make request
# r = requests.get(search_url, params={"q": "banana"}, timeout=5)
# # Print Result
# print("Requested URL:", r.url)
# print("Status:", r.status_code)
# print("Content type:", r.headers.get("Content-Type"))
# print("First 150 characters:", r.text[:150])

# # Trying a post request
# post_response = requests.post(
# 	search_url,
# 	data={"q": "apple"},
# 	timeout=5
# )
# # Print response
# print("POST status:", post_response.status_code)
# print("POST response length:", len(post_response.content))

# # Using a dictionary
# observation = {
# 	"method": "GET",
# 	"endpoint": "/rest/products/search",
# 	"status_code": r.status_code,
# 	"response_length": len(r.content),
# 	"content_type": r.headers.get("Content-Type")
# }
# print(observation)
# print("Status:", observation["status_code"])


# # Loops and lists
# records = []
# for term in ["apple", "banana"]:
# 	result = requests.get(search_url, params={"q": term}, timeout=5)
# 	records.append({"input": term, 
# 	                "status_code": result.status_code, 
# 	                "response_length": len(result.content)})
# print(records)

# def get_status(search_word):
# 	result = requests.get(search_url, params={"q": search_word}, timeout=5)
# 	return result.status_code
# print(get_status("apple"))
# print(get_status("banana"))

# try:
# 	test_response = requests.get(base_url, timeout=5)
# 	print("Connected. Status:", test_response.status_code)
# except requests.RequestException as error:
# 	print("Could not connect:", error)