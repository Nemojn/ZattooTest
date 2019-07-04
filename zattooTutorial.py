#library imports
import requests
import uuid
import json

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
helloResponse = sess.post('https://sandbox.zattoo.com/zapi/session/hello'+helloQuery)

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
watchResponse = json.loads(watchResponse.text)

#formats json object into more convenient form
print(json.dumps(watchResponse, indent=4, sort_keys=True))

#finds and prints stream url
print('Stream url: '+watchResponse['stream']['url'])
