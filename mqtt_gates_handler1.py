import time # The time library is useful for delays
import serial
import argparse

import paho.mqtt.client as mqtt # Import the MQTT library

publish_topic = "alert/gates"

def _insert_string(list_str,string,position):
	return list_str[:position] + [string] + list_str[position:]

def gates_parser():
    ''' construct argparse object for gates control '''
    parser = argparse.ArgumentParser()
    parser.add_argument('')


# Our "on message" event
def _message_function(client, userdata, message):
	global publish_topic
	topic = str(message.topic)
	command = str(message.payload.decode("utf-8"))
	topic_split=topic.split('/')


	if (topic_split[0]=="cmd" or topic_split[0]=="query"): #To avoid looping due to bridge
		if len(topic_split) == 3:
			#We have an ID number
			command+='\r\n'
			arduino.write(command.encode())
			publish_topic=topic+"/resp"
		else:
			ourClient.publish("alert/gates","Command sent to wrong topic: "+topic_split[0],2)


# Main program loop
if __name__ == '__main__':
	ourClient = mqtt.Client("python_script") # Create a MQTT client object
	ourClient.connect("localhost", 1883) # Connect to the test MQTT broker
	ourClient.subscribe("cmd/gates/#") # Subscribe to topics concerning gates
	ourClient.subscribe("query/gates/#")
	ourClient.on_message = _message_function # Attach the messageFunction to subscription
	ourClient.loop_start() # Start the MQTT client

	print('Running. Press CTRL-C to exit.')
	with serial.Serial("/dev/ttyACM0", 9600, timeout=5) as arduino:
		time.sleep(0.5) #wait for serial to open
		if arduino.isOpen():
			print("{} connected!".format(arduino.port))
			try:
				while True:
					while arduino.inWaiting()==0: pass
					if  arduino.inWaiting()>0:
						print("From ArdNano: "),
						answer=arduino.readline()
						print(answer),
						ourClient.publish(publish_topic,answer,2)
						#arduino.flushInput() #remove data after reading
			except KeyboardInterrupt:
				print("KeyboardInterrupt has been caught.")

