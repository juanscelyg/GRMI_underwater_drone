'''
VREP self-module
arm 
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017

@param sim_ip
	This parameter is the ip address where the simulation is running. It
	would be some address in the local net or the localhost, it should 
	be in string format and IPV4 version.

@param sim_port
	It is the port in the ip address where it is the simulation listening
	the data. Default is 19999, check the config simulation. 
'''
try:
    import GRMI_MUR.Simulate.vrep as vrep
except:
    print ('--------------------------------------------------------------')
    print ('There was a problem with imports. Check it, please.')
    print ('--------------------------------------------------------------')
    exit()

dic_sim_joint=dict()
dic_sim_joint[0]='MURA_joint1'
dic_sim_joint[1]='MURA_joint2'
dic_sim_joint[2]='MURA_joint3'
dic_sim_joint[3]='MURA_joint4'
dic_sim_joint[4]='MURA_joint5'
global clientID

def init(sim_ip,sim_port):
	global clientID
	vrep.simxFinish(-1) # just in case, close all opened connections
	clientID=vrep.simxStart(sim_ip,sim_port,True,True,5000,5) # Connect to V-REP
	if clientID!=-1:
		print ('Arm Simulation started')
		print ('Connected to remote API server')
		# Now send some data to V-REP in a non-blocking fashion:
		vrep.simxAddStatusbarMessage(clientID,'Simulating from outside . . .',vrep.simx_opmode_oneshot)
	else:
		print ('Failed connecting to remote API server')
		exit()
		
def SetTargetPosition(sim_joint,sim_value):
	global clientID
	# Here into the main code to move the robot
    errorCode,q1_motor_handle=vrep.simxGetObjectHandle(clientID,dic_sim_joint[sim_joint-1],vrep.simx_opmode_oneshot_wait)
    vrep.simxSetJointTargetPosition(clientID,q1_motor_handle,sim_value,vrep.simx_opmode_oneshot_wait)

def close():
	global clientID
    # Now send some data to V-REP in a non-blocking fashion:
    vrep.simxAddStatusbarMessage(clientID,'Simulation Finished!',vrep.simx_opmode_oneshot)
    # Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    vrep.simxGetPingTime(clientID)
    # Now close the connection to V-REP:
    vrep.simxFinish(clientID)
