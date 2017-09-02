'''
Code to connect the AWS and the robot
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017
'''
try:
    import GRMI_MUR.AWS.AWS_updater as AWS_updater
    import GRMI_MUR.Physical.RS485 as RS485
    import time
except:
    print ('--------------------------------------------------------------')
    print ('There was a problem with imports. Check it, please.')
    print ('--------------------------------------------------------------')
    exit()

AWS_updater.init(1)
RS485.init('/dev/ttyACM0', 9600)

### While loop to received info
try:
	while True:
		message_info=AWS_updater.aws_update_message()
		RS485.send(message_info)

except KeyboardInterrupt:
	RS485.close()
	exit()


