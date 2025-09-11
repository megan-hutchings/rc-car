import http.client

#connection = http.client.HTTPConnection("172.24.22.43", 8501)
connection = http.client.HTTPConnection("localhost", 8080)
connection.request("GET", "/")

response = connection.getresponse()
print("Status: {} and reason: {}".format(response.status, response.reason))

# Print the response body as text
print(response.read().decode())

connection.close()