'''
Arm
arm_parts 
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017
'''
import math
import numpy as np

def Getlength():
	l1=0.171
	l2=0.151
	l3=0.19117
	l4=0.043
	l=[l1,l2,l3,l4]
	return l
'''
	DH=[0       0       l1     -pi/2    0;
0       0       l2     0        0;
0       0       l2     0        0;
0       -l4     0     -pi/2     0;
0       l3      0      0        0];
'''	
def GetDH():
	l=Getlength()	
	DH=np.matrix([[0,0,l[0],-math.pi/2,0],[0,0,l[1],0,0],[0,0,l[1],0,0],[0,-l[3],0,-math.pi/2,0],[0,l[2],0,0,0]]);
	return DH
    
def GetDOF():
	return 5
	
def GetMass():
	m1=0.329
	m2=0.318 
	m3=0.318 
	m4=0.291 
	m5=0.399
	m=[m1, m2, m3, m4, m5]
	return m
	
	
