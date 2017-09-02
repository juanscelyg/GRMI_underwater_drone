'''
Code to connect AWS and the VREP simulation
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017
'''
try:
    import GRMI_MUR.AWS.AWS_updater as AWS_updater
    import GRMI_MUR.Simulate.arm as vrep_arm
    import time
except:
    print ('--------------------------------------------------------------')
    print ('There was a problem with imports. Check it, please.')
    print ('--------------------------------------------------------------')
    exit()

AWS_updater.init(1)
vrep_arm.init('192.168.4.104',19999)

### While loop to received info
try:
	while True:
		message_info=AWS_updater.aws_update_message()

except KeyboardInterrupt:
	exit()
