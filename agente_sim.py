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
    import GRMI_MUR.Arm.path616 as Path616
    import time
except:
    print ('--------------------------------------------------------------')
    print ('There was a problem with imports. Check it, please.')
    print ('--------------------------------------------------------------')
    exit()

### While loop to received info
AWS_updater.init(1)
vrep_arm.init('192.168.4.104',19999)
device_id=101

### While loop to received info
try:
	while True:
		message_info=AWS_updater.aws_update_message()
		if len(message_info) == AWS_updater.aws_size_frame():
			target_id,target_event, values=AWS_converter.aws2int(message_info)
			if device_id==target_id:
				if target_event==1:
					for i in range(1,len(values)+1):
						vrep_arm.SetTargetPosition(i,values[i-1])
						time.sleep(0.2)
				if target_event==2:
					q1,q2,q3,q4,q5=Inversekine.inversekine(values)
				if target_event==3:
					qs=Path616.planificador_616(x,y,z,theta,phi,Ttol,Tac,n)

except KeyboardInterrupt:
	exit()
