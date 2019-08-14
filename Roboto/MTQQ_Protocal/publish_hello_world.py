import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import numpy as np
import time
import json

data = np.full((4,4), 1)
data_list = data.tolist()
msg = json.dumps(data_list)

server = mqtt.Client()
server.connect('iot.eclipse.org')

while True:
	print(msg)
	msg = 'hello'
#	server.publish('topic_1', 'hey')
	publish.single('topic_1', 'hey', home)
	#server.loop()
#	time.sleep(1)
