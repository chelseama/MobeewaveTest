import requests
import urllib2
from flask import json

# get request to YUL airport
def get(url):
	content = urllib2.urlopen(url).read()
	return json.loads(content)

# post request to LHR airport
def post(url,jsonData):
	r = requests.post(url, json=jsonData)
	return json.loads(r.text)
