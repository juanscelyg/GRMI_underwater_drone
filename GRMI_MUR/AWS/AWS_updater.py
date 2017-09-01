'''
AWS Self-Module
AWS_update  
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017

@param mode
	mode==0 ---> update mode
	mode==1 ---> listen mode
	If you need to have two instances, you should type tow differente 
	codes, one to update the info in AWS and another to listen the
	new information updated in AWS.
'''
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import sys
import logging
import time
import json
import getopt
import socket

useWebsocket = False
host = "a2tn0cafpok0xk.iot.us-east-1.amazonaws.com"
rootCAPath = "VeriSignG5Key.pem"
certificatePath = "certificate_pem.crt"
privateKeyPath = "private_pem.key"
interface_socket = socket.socket()
arrival_message=''
mode=0

def init(_mode):
	global mode
	mode=_mode
	aws_check_config()
	aws_logger()
	if mode==0:
		init_aws_shadow_client_updater()
	if mode==1:
		init_aws_shadow_client_listener()
	config_aws_shadow_client()
	aws_connect()
	create_device_shadow()
	if mode==0:
		create_socket()

def aws_check_config():
	missingConfiguration = False
	if not host:
		print("Missing '-e' or '--endpoint'")
		missingConfiguration = True
	if not rootCAPath:
		print("Missing '-r' or '--rootCA'")
		missingConfiguration = True
	if not useWebsocket:
		if not certificatePath:
			print("Missing '-c' or '--cert'")
			missingConfiguration = True
		if not privateKeyPath:
			print("Missing '-k' or '--key'")
			missingConfiguration = True
	if missingConfiguration:
			exit(2)
			
def aws_logger():
	logger = logging.getLogger("AWSIoTPythonSDK.core")
	logger.setLevel(logging.DEBUG)
	streamHandler = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	streamHandler.setFormatter(formatter)
	logger.addHandler(streamHandler)
	
def init_aws_shadow_client_updater():
	global myAWSIoTMQTTShadowClient
	global rootCAPath
	global useWebsocket
	global host
	if useWebsocket:
		myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("basicShadowUpdater", useWebsocket=True)
		myAWSIoTMQTTShadowClient.configureEndpoint(host, 443)
		myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath)
	else:
		myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("basicShadowUpdater")
		myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
		myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
		
def init_aws_shadow_client_listener():
	global myAWSIoTMQTTShadowClient
	global rootCAPath
	global useWebsocket
	global host
	if useWebsocket:
		myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("basicShadowDeltaListener", useWebsocket=True)
		myAWSIoTMQTTShadowClient.configureEndpoint(host, 443)
		myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath)
	else:
		myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("basicShadowDeltaListener")
		myAWSIoTMQTTShadowClient.configureEndpoint(host, 8883)
		myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
		
def config_aws_shadow_client():
	global myAWSIoTMQTTShadowClient
	myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
	myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
	myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec
	
def aws_connect():
	global myAWSIoTMQTTShadowClient
	myAWSIoTMQTTShadowClient.connect()
	
def create_device_shadow():
	global myAWSIoTMQTTShadowClient
	global Bot
	global mode
	Bot = myAWSIoTMQTTShadowClient.createShadowHandlerWithName("Bot", True)
	if mode==0:
		Bot.shadowDelete(aws_customShadowCallback_Delete, 5)
	if mode==1:
		Bot.shadowRegisterDeltaCallback(aws_customShadowCallback_Delta)
	
def aws_customShadowCallback_Delta(payload, responseStatus, token):
	global arrival_message
	payloadDict = json.loads(payload)
	message_aux = str(payloadDict["state"]["property"])
	arrival_message=message_aux
	print("Received Message: " + message_aux)
	
def aws_update_message():
	global arrival_message
	return arrival_message
	
def aws_customShadowCallback_Update(payload, responseStatus, token):
	if responseStatus == "timeout":
		print("Update request " + token + " time out!")
	if responseStatus == "accepted":
		payloadDict = json.loads(payload)
	if responseStatus == "rejected":
		print("Update request " + token + " rejected!")

def aws_customShadowCallback_Delete(payload, responseStatus, token):
	if responseStatus == "timeout":
		print("Delete request " + token + " time out!")
	if responseStatus == "accepted":
		pass
	if responseStatus == "rejected":
		print("Delete request " + token + " rejected!")
		
def create_socket():
	global interface_socket
	sockethost =''
	socketport = 9191
	backlog = 5
	interface_socket.bind((sockethost,socketport))
	interface_socket.listen(backlog)
	print "//////////////////////////////////////////////////////////"
	print " \t Waiting for a connection"
	print "//////////////////////////////////////////////////////////"
	interface_socket, (sockethost,socketport) = interface_socket.accept()
	print"Socket Connected"
	print "//////////////////////////////////////////////////////////"
	
def close_socket():
	global interface_socket
	interface_socket.shutdown
	interface_socket.close
	
		
