from flask import Flask
from flask import request
from flask import abort
from flask import json
import requestToAirport
import json as JSON

app = Flask(__name__)

def process_response(responseData, isYUL):
	trackId = None
	if responseData['emergency']:
		return False,trackId
	print responseData
	if isYUL:
		count = responseData['numberOfPlaneAtTerminal']
		for track in responseData['landingTrack']:
			if track['occupied']:
				count += 1
			else:
				if trackId is None:
					trackId = track['landingTrackId']
		
	if not isYUL:
		count = responseData['numberOfGateOccupied']*responseData['totalNumberOfTerminal']
		for i,occupied in enumerate(responseData['planeOnTrack']):
			if occupied:
				count += 1
			else:
				if trackId is None:
					print responseData['planeOnTrack']
					trackId = responseData['landingTrackList'][i]['name']

	capacity = float(count)/responseData['totalNumberOfTerminal']
	if capacity > 0.9 or trackId is None:
		return False, None
	else:
		return True, trackId



@app.route('/v1/landing/authorization', methods=['POST'])
def response():
	if not request.json:
		abort(400)
	data = request.json
	if data['AirPort'].encode("utf8")=='YUL': 
		response = requestToAirport.get('http://yulairport.mobeewave-hive.com:8082/v1/traffic/portair1234')
		canLand, trackId = process_response(response, 1)
		
		if canLand:
			output = {'permissionGranted':'yes','trackId':trackId}
			return JSON.dumps(output)
		else:
			output = {'permissionGranted':'no','trackId':trackId}
			return JSON.dumps(output)

	if data["AirPort"]=="LHR": 
		response = requestToAirport.post('http://lhrairport.mobeewave-hive.com:8081/api/traffic',{"Username": "Portair","Password":"pa$$worD"})
		canLand,trackId = process_response(response, 0)
		# NOTE** trackId is hard-coded because there was no specification
		if canLand:
			output = {'permissionGranted':'yes','trackId':trackId}
			return JSON.dumps(output)
		else:
			output = {'permissionGranted':'no','trackId':trackId}
			return JSON.dumps(output)
	else:
		return abort(400)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

