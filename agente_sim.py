'''
Code to connect AWS and the VREP simulation
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017
'''
'''
try:
    import GRMI_MUR.AWS.AWS_updater as AWS_updater
    import GRMI_MUR.Simulate.arm as vrep_arm
    import GRMI_MUR.Common.converter as AWS_converter
    import GRMI_MUR.Arm.path616 as Path616
    import GRMI_MUR.Arm.kine as ARM_kine
    import time
except:
    print ('--------------------------------------------------------------')
    print ('There was a problem with imports. Check it, please.')
    print ('--------------------------------------------------------------')
    exit()
    '''
import GRMI_MUR.AWS.AWS_updater as AWS_updater
import GRMI_MUR.Simulate.arm as vrep_arm
import GRMI_MUR.Common.converter as AWS_converter
import GRMI_MUR.Arm.path616 as Path616
import GRMI_MUR.Arm.kine as ARM_kine
import time

### While loop to received info
AWS_updater.init(1)
vrep_arm.init('192.168.4.111',19999)
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
					q=ARM_kine.inversekine(values[0],values[1],values[2],values[3],values[4])
					for i in range(1,len(q)+1):
						vrep_arm.SetTargetPosition(i,q[i-1])
						time.sleep(0.2)
				if target_event==3:
					x=values[0];y=values[1];z=values[2];theta=values[3];phi=values[4]
					Ttol=30;Tac=2;n=30
					qs[:,:]=Path616.planificador_616(x,y,z,theta,phi,Ttol,Tac,n)

except KeyboardInterrupt:
	exit()
