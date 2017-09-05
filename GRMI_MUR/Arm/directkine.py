'''
Arm
directkine  
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017
'''

import GRMI_MUR.Arm.arm_parts as Arm_parts
import numpy as np
import math

DH=Arm_parts.GetDH()
num_dof=Arm_parts.GetDOF()
l=Arm_parts.Getlength()
l1=l[0]
l2=l[1]
l3=l[2]
l4=l[3]

def directkine(q1,q2,q3,q4,q5):
	c1=math.cos(q1)
	s1=math.sin(q1)
	A01=np.matrix([[c1,0,-s1,l1*c1],[s1,0,c1,l1*s1],[0,-1,0,0],[0,0,0,1]])
	c2=math.cos(q2)
	s2=math.sin(q2)
	A12=np.matrix([[c2,-s2,0,l2*c2],[s2,c2,0,l2*s2],[0,0,1,0],[0,0,0,1]])
	c3=math.cos(q3)
	s3=math.sin(q3)
	A23=np.matrix([[c3,-s3,0,l2*c3],[s3,c3,0,l2*s3],[0,0,1,0],[0,0,0,1]])
	c4=math.cos(q4)
	s4=math.sin(q4)
	A34=np.matrix([[c4,0,-s4,0],[s4,0,c4,0],[0,-1,0,-l4],[0,0,0,1]])
	c5=math.cos(q5)
	s5=math.sin(q5)
	A45=np.matrix([[c5,-s5,0,0],[s5,c5,0,0],[0,0,1,l3],[0,0,0,1]])
	return np.round(A01*A12*A23*A34*A45,4)
