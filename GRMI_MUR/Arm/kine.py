'''
Arm
kine  
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017

@param x 
	Global position in meters on axis X.
	
@param y
	Global position in meters on axis Y.
	
@param z
	Global position in meters on axis Z.
	
@param theta
	Global angle in degrees above axis Y.
	
@param phi
	Global angle in degrees above axis Z.
	
@param q1,q2,q3,q4,q5
	They are the generalized coordinates, these parameter can be received
	as individual values than as a values vector
'''

import GRMI_MUR.Arm.arm_parts as Arm_parts
import GRMI_MUR.Common.converter as rotations
import numpy as np
import math

def inversekine(x,y,z,theta,phi):
	l=Arm_parts.Getlength()
	l1=l[0]
	l2=l[1]
	l3=l[2]
	l4=l[3]
	A=rotations.roty(math.radians(theta))*rotations.roty(math.radians(phi));
	px=x;
	py=y;
	pz=z;
	#-------------------------------------------------------------------
	# Check points
	ux=A[0,0];uy=A[1,0];uz=A[2,0];
	distancia_planar=math.sqrt((px**2)+(py**2));
	distancia_planar_max=math.sqrt((l1+2*l2+l3)**2+(l4)**2);
	if distancia_planar>distancia_planar_max:
		print 'Cant access to the point.'
		q_f = [0,0,0,-math.pi/2,0];
	else:
		#-------------------------------------------------------------------------
		# Calc IK
		num_q1=-px+math.sqrt((-px)**2-(l4)**2+(py)**2);
		den_q1=py-l4;
		q1=2*math.atan2(num_q1,den_q1);
		q5=math.asin(ux*math.sin(q1)-uy*math.cos(q1));
		num_q234=(-uz/math.cos(q5));
		den_q234=((ux*math.cos(q1)+uy*math.sin(q1))/math.cos(q5));
		q234=math.atan2(num_q234,den_q234);
		k1=px*math.cos(q1)-l1+py*math.sin(q1)+l3*math.sin(q234);
		k2=pz-l3*math.cos(q234);
		var=round((((k1)**2+(k2)**2)/(2*(l2**2)))-1)
		q3=-math.acos(var); # Remember theta=-theta*
		sin_q2=(k2*(1+math.cos(q3))-k1*(math.sin(q3)))/(2*l2*(1+math.cos(q3)));
		cos_q2=(k1*(1+math.cos(q3))+k2*(math.sin(q3)))/(2*l2*(1+math.cos(q3)));
		q2=math.atan2(sin_q2,cos_q2);
		q4=q234-q2-q3;
		#-------------------------------------------------------------------------
		# Convert to toolbox references
		N=4;
		q2=-q2;
		q3=-q3;
		q4=-(q4+math.pi);
		q5=-q5;
		qf=[q1,q2,q3,q4,q5]
		for i in range(0,len(qf)):
			if qf[i]>math.pi:
				qf[i]=qf[i]-2*math.pi
			if qf[i]<-math.pi:
				qf[i]=qf[i]+2*math.pi
		q_f=round(qf[0],N)
		for i in range(1,len(qf)):
			q_f=np.append([q_f],[round(qf[i],N)])
	return q_f
	
def directkine(q1,q2,q3,q4,q5):
	DH=Arm_parts.GetDH()
	num_dof=Arm_parts.GetDOF()
	l=Arm_parts.Getlength()
	l1=l[0]
	l2=l[1]
	l3=l[2]
	l4=l[3]
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
	
def jacobiana_matrix(q1,q2,q3,q4,q5):
	DH=Arm_parts.GetDH()
	num_dof=Arm_parts.GetDOF()
	l=Arm_parts.Getlength()
	l1=l[0]
	l2=l[1]
	l3=l[2]
	l4=l[3]
	N=4
	j_1=np.array([[l4*math.cos(q1) - l1*math.sin(q1) - l2*math.cos(q2)*math.sin(q1) + l3*math.sin(q2 + q3 + q4)*math.sin(q1) - l2*math.cos(q2)*math.cos(q3)*math.sin(q1) + l2*math.sin(q1)*math.sin(q2)*math.sin(q3)],
			[l1*math.cos(q1) + l4*math.sin(q1) + l2*math.cos(q1)*math.cos(q2) - l3*math.sin(q2 + q3 + q4)*math.cos(q1) + l2*math.cos(q1)*math.cos(q2)*math.cos(q3) - l2*math.cos(q1)*math.sin(q2)*math.sin(q3)],
			[0],
			[0],
			[0],
			[1]]);
	j_2=np.array([[-math.cos(q1)*(l2*math.sin(q2 + q3) + l2*math.sin(q2) + l3*math.cos(q2 + q3 + q4))],
			[-math.sin(q1)*(l2*math.sin(q2 + q3) + l2*math.sin(q2) + l3*math.cos(q2 + q3 + q4))],
			[l3*math.sin(q2 + q3 + q4) - l2*math.cos(q2) - l2*math.cos(q2 + q3)],
			[-math.sin(q1)],
			[math.cos(q1)],
			[0]]);
	j_3=np.array([[-math.cos(q1)*(l2*math.sin(q2 + q3) + l3*math.cos(q2 + q3 + q4))],
			[-math.sin(q1)*(l2*math.sin(q2 + q3) + l3*math.cos(q2 + q3 + q4))],
			[l3*math.sin(q2 + q3 + q4) - l2*math.cos(q2 + q3)],
			[-math.sin(q1)],
			[math.cos(q1)],
			[0]]);	
	j_4=np.array([[-l3*math.cos(q2 + q3 + q4)*math.cos(q1)],
			[-l3*math.cos(q2 + q3 + q4)*math.sin(q1)],
			[l3*math.sin(q2 + q3 + q4)],
			[-math.sin(q1)],
			[math.cos(q1)],
			[0]]);
	j_5=np.array([[0],
			[0],
			[0],
			[-math.sin(q2 + q3 + q4)*math.cos(q1)],
			[-math.sin(q2 + q3 + q4)*math.sin(q1)],
			[-math.cos(q2 + q3 + q4)]]);
	J=np.concatenate((j_1, j_2), axis=1)
	J=np.concatenate((J, j_3), axis=1)
	J=np.concatenate((J, j_4), axis=1)
	J=np.concatenate((J, j_5), axis=1)
	#J=np.round(J,N);
	return J
