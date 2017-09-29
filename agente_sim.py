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
	import GRMI_MUR.Arm.move as arm_move
	import GRMI_MUR.Arm.kine as ARM_kine
	import numpy as np
	import matplotlib.pyplot as plt
	import time
except:
    print ('--------------------------------------------------------------')
    print ('There was a problem with imports. Check it, please.')
    print ('--------------------------------------------------------------')
    exit()

### While loop to received info
AWS_updater.SetAWSHost("a2tn0cafpok0xk.iot.us-east-1.amazonaws.com")
AWS_updater.SetAWSroot("VeriSignG5Key.pem")
AWS_updater.SetAWSCert("certificate_pem.crt")
AWS_updater.SetAWSKey("private_pem.key")
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
					Ttol=20;Tac=2.6;n=30
					qs,qp,qpp,tiempo=arm_move.planner_616(x,y,z,theta,phi,Ttol,Tac,n)
					qo=np.matrix([len(qs),Arm_parts.GetDOF()])
					for i in range(len(qs)):
						qo[i,:]=vrep_arm.GetPosition()
						for j in range(1,Arm_parts.GetDOF()+1):
							vrep_arm.SetTargetPosition(j,qs[i,j-1])
							time.sleep(0.02)
					plt.figure()
					plt.plot(tiempo,qs)
					plt.legend(('q1','q2','q3','q4','q5'))
					plt.show()
					plt.figure()
					plt.plot(tiempo,qo)
					plt.legend(('q1','q2','q3','q4','q5'))
					plt.show()
							

except KeyboardInterrupt:
	exit()
