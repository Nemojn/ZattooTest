#library imports
import requests
import uuid
import json
import socket
import urllib3

#setup uuid
deviceUUID = uuid.uuid4()
uuid_str = deviceUUID.urn
uuid_str = uuid_str[9:]
deviceUUID = uuid_str

#create session object
sess = requests.Session()

#setting up parameters to send in query
helloQuery = "?app_tid=7796241b-eb33-45f5-b677-76ff433b7663&uuid=" + deviceUUID + "&lang=en&format=json"

print('Starting session...')

#starts session
try:
	helloResponse = sess.post('https://sandbox.zattoo.com/zapi/session/hello'+helloQuery)
except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):
	print("Unable to connect to server. Check your internet connection")
else:
	#converts response to json object
	helloResponse = json.loads(helloResponse.text)
	
	#makes the json object nice and easy to read
	print(json.dumps(helloResponse, indent=4, sort_keys=True))
	
	#preparing watch query
	watchQuery = "?cid=3sat&stream_type=hls"
	
	print('Requesting stream url...')
	
	#requests stream url
	watchResponse = sess.post('https://sandbox.zattoo.com/zapi/watch'+watchQuery)
	
	#converts watch response into json object
	try:
		watchResponse = json.loads(watchResponse.text)
	except ValueError as e:
		print(watchResponse.text)
	else:
		#formats json object into more convenient form
		print(json.dumps(watchResponse, indent=4, sort_keys=True))
		
		if watchResponse['success'] is 'true':
			#finds and prints stream url
			print('Stream url: '+watchResponse['stream']['url'])
		else:
			httpError = str(watchResponse['http_status'])
			print("Unable to fetch watch URL. HTTP Error: "+httpError)
