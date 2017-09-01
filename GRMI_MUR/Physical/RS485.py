import serial
import time
import sys
RS485_port=None

def init(port_name,baudrate_port):
	global RS485_port
	RS485_port = serial.Serial(port_name, baudrate_port)
	if RS485_port.isOpen() == 0:
		RS485_port.open()
	time.sleep(1)

def send(message_string):
	global RS485_port
	RS485_port.write(message_string.encode())
	time.sleep(3)

def close():
	global RS485_port
	RS485_port.close()
