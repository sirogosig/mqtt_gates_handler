import paho.mqtt.client as mqtt # Import the MQTT library
import time # The time library is useful for delays
import serial

publish_topic = "alert/gates"

def insert_string(list_str,string,position):
	return list_str[:position] + [string] + list_str[position:]

# Our "on message" event
def messageFunction(client, userdata, message):
	global publish_topic
	topic = str(message.topic)
	message = str(message.payload.decode("utf-8"))
	topic_split=topic.split('/')

	if (topic_split[0]=="cmd") and (len(topic_split)== 4):
		#We have a command message with ID
		message_split=message.split(' ')
		if topic_split[2]=="servo0":
			command=insert_string(message_split,"0",1)
		if topic_split[2]=="servo1":
			command=insert_string(message_split,"1",1)
		if topic_split[2]=="servo2":
			command=insert_string(message_split,"2",1)
		command=' '.join(command)
		command+='\r\n'
		arduino.write(command.encode())
		publish_topic=topic+"/resp"
	elif (topic_split[0]=="query") and (len(topic_split)== 4):
		#We have a data query with ID
		message_split=message.split(' ')
		if topic_split[2]=="servo0":
			command=insert_string(message_split,"0",1)
		if topic_split[2]=="servo1":
			command=insert_string(message_split,"1",1)
		if topic_split[2]=="servo2":
			command=insert_string(message_split,"2",1)
		command=' '.join(command)
		command+='\r\n'
		arduino.write(command.encode())
		publish_topic=topic+"/resp"
	
	

ourClient = mqtt.Client("makerio_mqtt") # Create a MQTT client object
ourClient.connect("localhost", 1883) # Connect to the test MQTT broker
ourClient.subscribe("+/gates/#") # Subscribe to topics concerning gates
ourClient.on_message = messageFunction # Attach the messageFunction to subscription
ourClient.loop_start() # Start the MQTT client

# Main program loop
if __name__ == '__main__':
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

