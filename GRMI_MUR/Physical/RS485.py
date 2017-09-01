import serial
import time
import sys

def init(port_name,baudrate_port):
	RS485_port = serial.Serial(port_name, baudrate_port)
	if RS485_port.isOpen() == 0:
		RS485_port.open()
	time.sleep(1)

def send(message_string):
	RS485_port.write(message_string.encode())
	time.sleep(3)

def close():
	RS485_port.close()
