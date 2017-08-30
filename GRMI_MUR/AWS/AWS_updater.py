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
myAWSIoTMQTTShadowClient = None
Bot = None
interface_socket = socket.socket()

def iniciar():
	aws_check_config()
	aws_logger()
	init_aws_shadow_client()
	config_aws_shadow_client()
	aws_connect()
	create_device_shadow()
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
	
def init_aws_shadow_client():
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
	Bot = myAWSIoTMQTTShadowClient.createShadowHandlerWithName("Bot", True)
	Bot.shadowDelete(aws_customShadowCallback_Delete, 5)
	
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
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Delete request with token: " + token + " accepted!")
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
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
	
		
