'''
Test to conect the robot to mov


'''
try:
	import GRMI_MUR.AWS.AWS_updater as AWS_updater
	import time
except:
    print ('--------------------------------------------------------------')
    print ('There was a problem with the import. Check it please.')
    print ('--------------------------------------------------------------')
    exit()

AWS_updater.iniciar()
# Update shadow in a loop
try:
	while True:
		mensaje = AWS_updater.interface_socket.recv(8)
		mensaje = mensaje + "\n"
		print mensaje
		JSONPayload = '{"state":{"desired":{"property":' + str(mensaje) + '}}}'
		AWS_updater.Bot.shadowUpdate(JSONPayload, AWS_updater.aws_customShadowCallback_Update, 5)
		time.sleep(1)
except KeyboardInterrupt:
	AWS_updater.close_socket()
	exit()
	
finally:
	AWS_updater.close_socket()
	exit()
	
		 
