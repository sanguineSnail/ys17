import socket               # Import socket module
import RPi.GPIO as gpio
import time

#init

gpio.setmode(gpio.BOARD)

chOutMotor = 35 	# MOTOR
chOutSensor = 37 	# RED DIODE
chOutButton = 36	# YELLOW DIODE
chOutMain = 40		# GREEN DIODE

gpio.setup(chOutMotor, gpio.OUT)
gpio.setup(chOutSensor, gpio.OUT) 
gpio.setup(chOutButton, gpio.OUT)
gpio.setup(chOutMain, gpio.OUT)

gpio.output(chOutMain, True) # Main program starts

SIZE = 1024 # Socket input buffer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#host = socket.gethostname() # Get local machine name server
HOST = "192.168.3.1"
PORT = 52811               # Reserve a port for your service.
s.bind((HOST, PORT))        # Bind to the port
s.listen(5)                 # Now wait for client connection.
#main

client, addr = s.accept()     # Establish connection with client.
print ('Got connection from', addr)

press = False
smoke = False
msgcounter = 0
while True:
	data = client.recv(SIZE)
	msgcounter += 1
	print(str(msgcounter) + "  MSG=" + data)
	press = False
	smoke = False
	if data == "Both":
		press = True
		smoke = True
	elif data == "Smoke":
		smoke = True
	elif data == "Press":
		press = True
	elif data == "Nothing":
		pass
	elif data == "OVER":
		break
	else:
		print("Bad message: " + data)
	if press == True:
		gpio.output(chOutButton, True)		
	else: 
		gpio.output(chOutButton, False)	

	if smoke == True:
		gpio.output(chOutMotor, True)
		gpio.output(chOutSensor, True)		
	else: 
		gpio.output(chOutMotor, False)
		gpio.output(chOutSensor, False)	

#clean
s.close() 

gpio.output(chOutMain, False) #Main program ends
gpio.output(chOutMotor, False)
gpio.output(chOutSensor, False)
gpio.output(chOutButton, False)

gpio.cleanup(chOutMain)
gpio.cleanup(chOutMotor)
gpio.cleanup(chOutSensor)
gpio.cleanup(chOutButton)
