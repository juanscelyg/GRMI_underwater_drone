import GRMI_MUR.Arm.arm_parts as Arm_parts
import GRMI_MUR.AWS.AWS_updater as AWS_updater
import GRMI_MUR.Arm.kine as Arm_kine
import GRMI_MUR.Arm.path616 as Path616
import GRMI_MUR.Simulate.arm as vrep_arm
import GRMI_MUR.Common.converter as AWS_converter
import time

x=0.1534
y=-0.0430
z=0.4129
theta=30
phi=-38.33
'''
x=0.6402
y=-0.0281
z=0.0839
theta=83.33
phi=-140
'''
q1,q2,q3,q4,q5=Arm_kine.inversekine(x,y,z,theta,phi)
print q1
print q2
print q3
print q4
print q5
DH=Arm_parts.GetDH()
print DH
num_dof=Arm_parts.GetDOF()
print num_dof
values=Arm_kine.directkine(q1,q2,q3,q4,q5)
print values
j=Arm_kine.jacobiana_matrix(q1,q2,q3,q4,q5)
print j
'''
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
					q=Arm_kine.inversekine(values[0],values[1],values[2],values[3]/10,values[4]/10)
				if target_event==3:
					qs=Path616.planificador_616(x,y,z,theta,phi,Ttol,Tac,n)

except KeyboardInterrupt:
	exit()
'''
