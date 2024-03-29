#library imports
import requests
import uuid
import json
import socket
import urllib3

#importing secret app id
from SecretParams import *

#status boolean initialization
internetConnection = False
helloSuccessful = False
watchSuccessful = False
disabledChannel = False
endedSession = False

#http error indicators
helloError = "null"
watchError = "null"
streamURL = "null"
disableError = "null"
endError = "null"


#creates uuid
deviceUUID = uuid.uuid4()
uuid_str = deviceUUID.urn
uuid_str = uuid_str[9:]
deviceUUID = uuid_str

#create session object
sess = requests.Session()

#setting up parameters to send in query
helloQuery = "?app_tid=" + app_tid + "&uuid=" + deviceUUID + "&lang=en&format=json"

print('Starting session...')

#starts session
try:
	helloResponse = sess.post('https://sandbox.zattoo.com/zapi/session/hello'+helloQuery)
	#converts response into JSON object
	helloResponse = json.loads(helloResponse.text)
#error handling for no internet connection
except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):
	internetnetConnection = False
	print("Unable to connect to server. Check your internet connection")
except ValueError:
	internetConnection = True
	print("Error: Response not in JSON format.")
else:
	internetConnection = True
	
	#makes the json object nice and easy to read
	print(json.dumps(helloResponse, indent=4, sort_keys=True))
	if helloResponse['success'] is False:
		try:
			helloError = str(helloResponse['http_status'])
		except KeyError:
			helloError = "none"
	else:
		helloSuccessful = True
		helloError = "none"
		print('Successfully connected to server.')
		
		#preparing watch query
		watchQuery = "?cid=3sat&stream_type=hls"
		print('Requesting stream url...')
		
		#requests stream url
		try:
			watchResponse = sess.post('https://sandbox.zattoo.com/zapi/watch'+watchQuery)
			
			#converts watch response into json object
			watchResponse = json.loads(watchResponse.text)
		except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):
			internetConnection = False
			print("Unable to connect to server. Check your internet connection.")
		except ValueError:
			print("Error: Response not in JSON format.")
		else:
			#formats json object into more convenient form
			print(json.dumps(watchResponse, indent=4, sort_keys=True))
			
			if watchResponse['success'] is False:
				try:
					watchError = str(watchResponse['http_status'])
					print("Unable to fetch watch URL. HTTP Error: " + watchError)
				except KeyError:
					watchError = "none"
			else:
				watchSuccessful = True
				watchError = "none"
				
				#finds and prints stream url
				streamURL = watchResponse['stream']['url']
				print('Stream URL: ' + streamURL)
				
				#stopping test channel
				print('Stopping test channel...')
				try:
					stopResponse = sess.get('https://sandbox.zattoo.com/zapi/stop')
					stopResponse = json.loads(stopResponse.text)
				except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):
					internetnetConnection = False
					print("Unable to connect to server. Check your internet connection")
				except ValueError:
					internetConnection = True
					print("Error: Response not in JSON format.")
				else:
					if stopResponse['success'] is False:
						try:
							disableError = str(stopResponse['http_status'])
							print("An error occured while attempting to stop the test channel. HTTP Error: " + stopError)
						except KeyError:
							stopError = "none"
					else:
						disabledChannel = True
						disableError = "none"
			
						print(json.dumps(watchResponse, indent=4, sort_keys=True))
						print('Test channel stopped.')
		finally:
			#stopping session
			print('Stopping session...')
			try:
				stopSessionResponse = sess.post('https://sandbox.zattoo.com/zapi/session/goodbye')
				stopSessionResponse = json.loads(stopSessionResponse.text)
			except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.ConnectionError):
				internetnetConnection = False
				print("Unable to connect to server. Check your internet connection")
			except ValueError:
				internetConnection = True
				print("Error: Response not in JSON format.")
			else:
				if stopSessionResponse['success'] is False:
					try:
						endError = str(stopSessionResponse['http_status'])
						print("An error occured while attempting to end the session. HTTP Error: " + endError)
					except KeyError:
						endError = "none"
				else:
					endedSession = True
					endError = "none"
					print(json.dumps(stopSessionResponse, indent=4, sort_keys=True))
					print('Session stopped.')
finally:
	#Status report printing
	print("\nStatus:\n\nConnected to internet: " + str(internetConnection) + "\nHello call successful: " + str(helloSuccessful) + 
	"\nWatch call successful: " + str(watchSuccessful) + "\nChannel disabled: " + str(disabledChannel) + "\nSession stopped: " + str(endedSession) + "\nStream URL: " + streamURL)
	
	print("\nHTTP Errors:\n\nHello call error: " + helloError + "\nWatch call error: " + watchError + "\nDisable channel error: " + disableError + "\nEnd session error: " + endError)
