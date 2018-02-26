import requests
import json


r = requests.post("http://0.0.0.0:5000/v1/landing/authorization", json={"AirPort": "YUL","FlightNumber":"MR100"})
print(r.text)