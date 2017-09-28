'''
Arm
move 
@version 0.1
@author Juan Cely <juanscelyg@gmail.com>
Research Group of Robots and Intelligent Machines
Date: August/2017
'''
import GRMI_MUR.Arm.arm_parts as Arm_parts
import GRMI_MUR.Arm.kine as Arm_kine
import GRMI_MUR.Simulate.arm as vrep_arm
import math
import numpy as np

def planner_616(x,y,z,theta,phi,Ttol,Tac,n):
	Ttol=float(Ttol)
	Tac=float(Tac)
	if n<10:
		n=10;
	qo=vrep_arm.GetPosition()
	qf=Arm_kine.inversekine(x,y,z,theta,phi)
	dt=Ttol/(n)
	dq=np.empty(len(qo))
	for i in range(0,len(qo)):
		dq[i]=(qf[i]-qo[i])/(n)
	tiempo=np.arange(0.0,Ttol,dt)
	q=np.empty([len(tiempo),len(qo)])
	q[0,:]=qo
	for i in range(1,len(tiempo)):
		q[i,:]=q[i-1,:]+dq
	qp=np.diff(q,axis=0)
	Vmax=np.empty(len(qo))
	for i in range(len(qo)):
		Vmax[i]=dq[i]/dt
	#Soft
	#q soft
	qs=np.empty([len(tiempo),len(qo)])
	qs[0,:]=qo;
	for j in range(0,len(qo)):
		q_o=qo[j]
		for i in range(1,len(tiempo)):
			if tiempo[i]<=Tac:
				t=tiempo[i]
				a0=q_o
				a1=0
				a2=0
				a3=0
				a4=(5/(2*(math.pow(Tac,3))))*Vmax[j]
				a5=(-3/(math.pow(Tac,4)))*Vmax[j]
				a6=(1/(math.pow(Tac,5)))*Vmax[j]
				qs[i,j]=(a6*(math.pow(t,6)))+(a5*(math.pow(t,5)))+(a4*(math.pow(t,4)))+(a3*(math.pow(t,3)))+(a2*(math.pow(t,2)))+(a1*t)+a0
			elif tiempo[i]>=Tac and tiempo[i]<(Ttol-Tac):
				t=tiempo[i]-Tac
				b0=q_o+((Tac/2)*Vmax[j])
				b1=Vmax[j]
				qs[i,j]=(b1*t)+b0
			elif tiempo[i]>=(Ttol-Tac):
				t=tiempo[i]-(Ttol-Tac)
				c0=(Ttol-(3.0/2)*Tac)*Vmax[j]+q_o
				c1=Vmax[j]
				c2=0
				c3=0
				c4=(-5/(2*(math.pow(Tac,3))))*Vmax[j]
				c5=(3/(math.pow(Tac,4)))*Vmax[j]
				c6=(-1/(math.pow(Tac,5)))*Vmax[j]
				qs[i,j]=(c6*(math.pow(t,6)))+(c5*(math.pow(t,5)))+(c4*(math.pow(t,4)))+(c3*(math.pow(t,3)))+(c2*(math.pow(t,2)))+(c1*t)+c0
	# To velocity
	qp_0=np.diff(qs, axis=0)
	limite=np.round(len(qp_0)/2,0)
	qp_1=qp_0[0:limite-1,:]
	qp_2=qp_0[limite:len(qp_0),:]
	qp_s=np.concatenate((qp_1,qp_2), axis=0)
	qp_s=np.insert(qp_s, len(qp_s), [0, 0, 0, 0, 0],axis=0)
	qp_s=np.insert(qp_s, 0, [0, 0, 0, 0, 0],axis=0)	
	# To acc
	qpp_0=np.diff(qp_s, axis=0)
	limite=np.round(len(qpp_0)/2,0)
	qpp_1=qpp_0[0:limite-1,:]
	qpp_2=qpp_0[limite:len(qpp_0),:]
	qpp_s=np.concatenate((qpp_1,qpp_2), axis=0)
	qpp_s=np.insert(qpp_s, len(qpp_s), [0, 0, 0, 0, 0],axis=0)
	qpp_s=np.insert(qpp_s, 0, [0, 0, 0, 0, 0],axis=0)	
	return np.round(qs,4), np.round(qp_s,4), np.round(qpp_s,4), np.round(tiempo,4)
	
