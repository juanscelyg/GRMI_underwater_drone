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
    import GRMI_MUR.Common.converter as AWS_converter
    import time
except:
    print ('--------------------------------------------------------------')
    print ('There was a problem with imports. Check it, please.')
    print ('--------------------------------------------------------------')
    exit()

AWS_updater.init(1)
vrep_arm.init('192.168.4.104',19999)
device_id=101

### While loop to received info
try:
	while True:
		message_info=AWS_updater.aws_update_message()
		if len(message_info) == AWS_updater.aws_size_frame():
			target_id,target_event, values=AWS_converter.aws2int()
			if device_id==target_id:
				if target_event==1:
					for i in range(1,len(values)+1):
						vrep_arm.SetJointPosition(i,values[i-1])
						time.sleep(0.2)

except KeyboardInterrupt:
	exit()
