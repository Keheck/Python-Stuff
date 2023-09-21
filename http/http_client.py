import http.client
import ssl

client = http.client.HTTPConnection("10.6.4.0", 80, 5, ("10.254.0.170", 80))

client.connect()
client.request("POST", "/index.html", '{foo: "bar"}', {"Content-Type": "application/json", "Accept": "application/json"})
res = client.getresponse()
print(res.status, res.reason)
