'''
Common
converter  
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017

@param message_info 
	It is the incomming string from AWS, it has a lenght above 24 digits
	but the functions reads this parameter as string.
	
@param target_id
	It is a three digits number, this number identifiers the ID
	
@param target_event
	It is a assigment number, it must value between 0-9
	
@param param
	It is a list, where it has the information above 5 parameters. These
	numbers must be integers, the operation doesnt support another format
	numbers.
	
@param ang
	It it the ang in radians to do the rotation.
'''
import math
import numpy as np

def aws2int(message_info):
	param=[0,0,0,0,0]
	param_out=[0,0,0,0,0]
	sense=[0,0,0,0,0]
	target_id=int(message_info[0:3])
	target_event=int(message_info[3])
	param[0]=int(message_info[4:7])
	sense[0]=int(message_info[7])
	param[1]=int(message_info[8:11])
	sense[1]=int(message_info[11])
	param[2]=int(message_info[12:15])
	sense[2]=int(message_info[15])
	param[3]=int(message_info[16:19])
	sense[3]=int(message_info[19])
	param[4]=int(message_info[20:23])
	sense[4]=int(message_info[23])
	for i in range(0,len(sense)):
		if sense[i]==1:
			param_out[i]=-param[i]
		else:
			param_out[i]=param[i]
	return target_id,target_event,param_out
	
	
def int2aws(target_id,target_event,param):
	sense=[0,0,0,0,0]
	message_info=''
	for i in range(0,len(sense)):
		if param[i]<0:
			param[i]=int(math.fabs(param[i]))
			sense[i]=1
		if param[i]>99:
			message_info=message_info+str(param[i])+str(sense[i])
		else:
			if param[i]>9:
				message_info=message_info+str(0)+str(param[i])+str(sense[i])
			else:
				message_info=message_info+str(0)+str(0)+str(param[i])+str(sense[i])
	message_head=str(target_id)+str(target_event)
	message_out=message_head+message_info
	return message_out

def roty(ang):
	ct = math.cos(ang);
	st = math.sin(ang);
	R=np.matrix([[ct,0,st],[0,1,0],[-st,0,ct]])
	return R
	
def rotz(ang):
	ct = math.cos(ang);
	st = math.sin(ang);
	w,h=3,3;
	R=np.matrix([[ct,-st,0],[st,ct,0],[0,0,1]])
	return R
	
	
	
