'''
Arm
dynamic  
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017
'''
import GRMI_MUR.Arm.arm_parts as Arm_parts
import GRMI_MUR.Arm.directkine as kine
import numpy as np
import math

DH=Arm_parts.GetDH()
num_dof=Arm_parts.GetDOF()
l=Arm_parts.Getlength()
l1=l[0]
l2=l[1]
l3=l[2]
l4=l[3]
m=Arm_parts.GetMass()
m1=m[0]
m2=m[1]
m3=m[2]
m4=m[3]
m5=m[4]

def torques(q,qp,qpp,fe):
	q1=q[0];
	q2=q[1];
	q3=q[2];
	q4=q[3];
	q5=q[4];
	qp1=qp[0];
	qp2=qp[1];
	qp3=qp[2];
	qp4=qp[3];
	qp5=qp[4];
	qpp1=qpp[0];
	qpp2=qpp[1];
	qpp3=qpp[2];
	qpp4=qpp[3];
	qpp5=qpp[4];
	fx=fe[0];
	fy=fe[1];
	fz=fe[2];
	nx=fe[3];
	ny=fe[4];
	nz=fe[5];
	## N-E 1
	A01=np.matrix([[cos(q1), 0,          -sin(q1),     l1*cos(q1)], [sin(q1),   0,         cos(q1),     l1*sin(q1)], [0, -1, 0, 0],   [0, 0, 0, 1]]);
	A12=np.matrix([[cos(q2), -sin(q2),   0,            l2*cos(q2)], [sin(q2),   cos(q2),   0,           l2*sin(q2)], [0, 0,  1, 0],   [0, 0, 0, 1]]);
	A23=np.matrix([[cos(q3), -sin(q3),   0,            l2*cos(q3)], [sin(q3),   cos(q3),   0,           l2*sin(q3)], [0, 0,  1, 0],   [0, 0, 0, 1]]);
	A34=np.matrix([[cos(q4), 0,          -sin(q4),     0],          [sin(q4),   0,         cos(q4),     0],          [0, -1, 0, -l4], [0, 0, 0, 1]]);
	A45=np.matrix([[cos(q5), -sin(q5),   0,            0],          [sin(q5),   cos(q5),   0,           0],          [0, 0,  1, l3],  [0, 0, 0, 1]]);
	## N-E 2
	wx0=0; 
	wy0=0; 
	wz0=0; 
	wpx0=0; 
	wpy0=0; 
	wpz0=0; 
	vx0=0; 
	vy0=0; 
	vz0=0; 
	vpx0=0; 
	vpy0=0;
	g=9.81;
	# Base Velocity
	w00=np.matrix([[wx0],[wy0],[wz0]]);
	wp00=np.matrix([[wpx0],[wpy0],[wpz0]]);
	v00=np.matrix([[vx0],[vy0],[vz0]]);
	vp00=np.matrix([[vpx0],[vpy0],[-g]]);
	# Forces and Torques Vectors
	f66=np.matrix([[fx],[fy],[fz]]);
	n66=np.matrix([[nx],[ny],[nz]]);
	# Set Positions and inertials
	z0=np.matrix([[0],[0],[1]]);
	p11=np.matrix([[l1],[0],[0]]);
	p22=np.matrix([[l2],[0],[0]]);
	p33=np.matrix([[l2],[0],[0]]);
	p44=np.matrix([[0],[-l4*sin(-pi/2)],[-l4*cos(-pi/2)]]);
	p55=np.matrix([[0],[l3*sin(0)],[l3*cos(0)]]);
	# Centers distance
	s11x=0.041007;	s11y=-0.017564;	s11z=0.015976;
	s22x=0.036678;	s22y=-0.018167;	s22z=-0.016524;
	s33x=0.036678;	s33y=0.018167;	s33z=0.016524;
	s44x=0.027035;	s44y=-0.019879;	s44z=0.011106;
	s55x=0.014492;	s55y=-0.024296;	s55z=0.05929;
	s11=np.matrix([[s11x],[s11y],[s11z]]);
	s22=np.matrix([[s22x],[s22y],[s22z]]);
	s33=np.matrix([[s33x],[s33y],[s33z]]);
	s44=np.matrix([[s44x],[s44y],[s44z]]);
	s55=np.matrix([[s55x],[s55y],[s55z]]);
	I=np.identity(3)
	## N-E 3
	A01=kine.directkine_A01(q1)
	A12=kine.directkine_A12(q2)
	A23=kine.directkine_A23(q3)
	A34=kine.directkine_A34(q4)
	A45=kine.directkine_A45(q5)	
	R01=A01[np.ix_([0,3],[0,3])]
	R12=A12[np.ix_([0,3],[0,3])]
	R23=A23[np.ix_([0,3],[0,3])]
	R34=A34[np.ix_([0,3],[0,3])]
	R45=A45[np.ix_([0,3],[0,3])]
	R05=np.round(R01*R12*R23*R34*R45,4)
	R10=np.linalg.inv(R01);
	R21=np.linalg.inv(R12);
	R32=np.linalg.inv(R23);
	R43=np.linalg.inv(R34);
	R54=np.linalg.inv(R45);
	R50=np.linalg.inv(R05);
	## N-E 4
	w11=R10*(w00+z0*qp1);
	w22=R21*(w11+z0*qp2);
	w33=R32*(w22+z0*qp3);
	w44=R43*(w33+z0*qp4);
	w55=R54*(w44+z0*qp5);
	## N-E 5
	wp11=R10*(wp00+z0*qpp1)+np.cross(w00,(z0*qp1));
	wp22=R21*(wp11+z0*qpp2)+np.cross(w11,(z0*qp2));
	wp33=R32*(wp22+z0*qpp3)+np.cross(w22,(z0*qp3));
	wp44=R43*(wp33+z0*qpp4)+np.cross(w33,(z0*qp4));
	wp55=R54*(wp44+z0*qpp5)+np.cross(w44,(z0*qp5));
	## N-E 6
	vp11=np.cross(wp11,p11)+np.cross(w11,np.cross(w11,p11))+R10*vp00;
	vp22=np.cross(wp22,p22)+np.cross(w22,np.cross(w22,p22))+R21*vp11;
	vp33=np.cross(wp33,p33)+np.cross(w33,np.cross(w33,p33))+R32*vp22;
	vp44=np.cross(wp44,p44)+np.cross(w44,np.cross(w44,p44))+R43*vp33;
	vp55=np.cross(wp55,p55)+np.cross(w55,np.cross(w55,p55))+R54*vp44;
	## N-E 7
	a11=np.cross(wp11,s11)+np.cross(w11,np.cross(w11,s11))+vp11;
	a22=np.cross(wp22,s22)+np.cross(w22,np.cross(w22,s22))+vp22;
	a33=np.cross(wp33,s33)+np.cross(w33,np.cross(w33,s33))+vp33;
	a44=np.cross(wp44,s44)+np.cross(w44,np.cross(w44,s44))+vp44;
	a55=np.cross(wp55,s55)+np.cross(w55,np.cross(w55,s55))+vp55;
	## N-E 8
	f55=R50*f66+m5*a55;
	f44=R45*f55+m4*a44;
	f33=R34*f44+m3*a33;
	f22=R23*f33+m2*a22;
	f11=R12*f22+m1*a11;
	## N-E 9
	n55=R50*(n66+np.cross((R05*p55),f66))+np.cross((p55+s55),(m5*a55))+I*wp55+np.cross(w55,(I*w55));
	n44=R45*(n55+np.cross((R54*p44),f55))+np.cross((p44+s44),(m4*a44))+I*wp44+np.cross(w44,(I*w44));
	n33=R34*(n44+np.cross((R43*p33),f44))+np.cross((p33+s33),(m3*a33))+I*wp33+np.cross(w33,(I*w33));
	n22=R23*(n33+np.cross((R32*p22),f33))+np.cross((p22+s22),(m2*a22))+I*wp22+np.cross(w22,(I*w22));
	n11=R12*(n22+np.cross((R21*p11),f22))+np.cross((p11+s11),(m1*a11))+I*wp11+np.cross(w11,(I*w11));
	## N-E 10
	T5=(n55.transpose())*R54*z0;
	T4=(n44.transpose())*R43*z0;
	T3=(n33.transpose())*R32*z0;
	T2=(n22.transpose())*R21*z0;
	T1=(n11.transpose())*R10*z0;
	tau=np.matrix([[T1],[T2],[T3],[T4],[T5]]);
	return tau
	
	
	
	
	 
