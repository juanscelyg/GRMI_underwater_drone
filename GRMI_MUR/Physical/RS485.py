'''
Physical Module
RS485  
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017

@param port_name
	It is the port name, in string format. For example, if you are using
	MS Windows with the COM3 and 9600 baudrate, the code will be as: 
	GRMI_MUR.Physical.RS485.init('COM3',9600)
@param baudrate_port
	It is the port baudrate. Remember all operativ system has differents
	baudrate to work correctly. Check the os documentation. 
'''
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
