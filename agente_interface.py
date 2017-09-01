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
    print ('There was a problem with the import. Check it please.')
    print ('--------------------------------------------------------------')
    exit()

AWS_updater.init(0)
try:
	while True:
		mensaje = AWS_updater.interface_socket.recv(8)
		mensaje = mensaje + "\n"
		print ('--------------------------------------------------------------')
		print mensaje
		print ('--------------------------------------------------------------')
		JSONPayload = '{"state":{"desired":{"property":' + str(mensaje) + '}}}'
		AWS_updater.Bot.shadowUpdate(JSONPayload, AWS_updater.aws_customShadowCallback_Update, 5)
		time.sleep(1)
except KeyboardInterrupt:
	AWS_updater.close_socket()
	exit()
	
finally:
	AWS_updater.close_socket()
	exit()
	
		 
