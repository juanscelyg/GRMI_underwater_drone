'''
Code to connect the interface with the updater AWS
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017
'''
try:
	import GRMI_MUR.AWS.AWS_updater as AWS_updater
	import time
except:
    print ('--------------------------------------------------------------')
    print ('There was a problem with imports. Check it, please.')
    print ('--------------------------------------------------------------')
    exit()

AWS_updater.init(0)
while True:
	mensaje = AWS_updater.interface_socket.recv(AWS_updater.aws_size_frame())
	print ('--------------------------------------------------------------')
	print mensaje
	print ('--------------------------------------------------------------')	
	AWS_updater.Bot.shadowUpdate(AWS_updater.aws_create_payload(mensaje), AWS_updater.aws_customShadowCallback_Update, 5)
	time.sleep(1)
