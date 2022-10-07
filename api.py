import requests
import json

request_url = "http://192.168.29.229:5000/target"
fetch = requests.get(request_url)
data = json.loads(fetch.text)
print(data)
