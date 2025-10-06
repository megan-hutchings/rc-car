import http.client

connection = http.client.HTTPConnection("192.168.137.191", 80)



connection.request("GET", "/")

response = connection.getresponse()
print("Status: {} and reason: {}".format(response.status, response.reason))

# Print the response body as text
print(response.read().decode())

connection.close()