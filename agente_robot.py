'''
Test to conect the robot to mov
'''
try:
    import GRMI_MUR.Simulate.vrep as vrep
    import GRMI_MUR.AWS.AWS_updater as AWS_updater
    import GRMI_MUR.Physical.RS485 as RS485
    import time
except:
    print ('--------------------------------------------------------------')
    print ('There Was a problem with the import. Check it please.')
    print ('--------------------------------------------------------------')
    exit()

AWS_updater.init(1)
RS485.init('/dev/ttyACM0', 9600)
try:
	while True:
		pass

except KeyboardInterrupt:
	RS485.close()
	exit()
#'''
#print ('Program started')
#vrep.simxFinish(-1) # just in case, close all opened connections
#clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to V-REP
#if clientID!=-1:
    #print ('Connected to remote API server')

    ## Now try to retrieve data in a blocking fashion (i.e. a service call):
    #res,objs=vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_blocking)
    #if res==vrep.simx_return_ok:
        #print ('Number of objects in the scene: ',len(objs))
    #else:
        #print ('Remote API function call returned with error code: ',res)

    #time.sleep(2)

    ## Now send some data to V-REP in a non-blocking fashion:
    #vrep.simxAddStatusbarMessage(clientID,'Simulating . . .',vrep.simx_opmode_oneshot)

	## Here into the main code to move the robot
    #errorCode,q1_motor_handle=vrep.simxGetObjectHandle(clientID,'MURA_joint3',vrep.simx_opmode_oneshot_wait)
    #print errorCode
    #vrep.simxSetJointTargetPosition(clientID,q1_motor_handle,45,vrep.simx_opmode_oneshot_wait)

    ## Now send some data to V-REP in a non-blocking fashion:
    #vrep.simxAddStatusbarMessage(clientID,'Bye!',vrep.simx_opmode_oneshot)

    ## Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    #vrep.simxGetPingTime(clientID)

    ## Now close the connection to V-REP:
    #vrep.simxFinish(clientID)
#else:
    #print ('Failed connecting to remote API server')
#print ('Program ended')
#'''

