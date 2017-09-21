import GRMI_MUR.Arm.arm_parts as Arm_parts
import GRMI_MUR.Arm.kine as Arm_kine
import GRMI_MUR.Simulate.arm as vrep_arm
import math
import numpy as np

def planner_616(x,y,z,theta,phi,Ttol,Tac,n):
	if n<10:
		n=10;
	qo=vrep_arm.GetPosition()
	qf=Arm_kine.inversekine(x,y,z,theta,phi)
	dq=np.arange(5, dtype=np.float)
	dq[0]=(qo[0]-qf[0])/(n+1)
	for i in range(1,len(qo)):
		dq[i]=(qo[i]-qf[i])/(n+1);
	q=np.indices(n+1, len(qo))
	q[0,:]=qo;
	dt=Ttol/(n+1);
	tiempo=np.arange(n+1, dtype=np.float)
	for i in range(1,n+1):
		q[i,:]=(q[i-1,:]-dq)
	for i in range(1,n+1):
	    tiempo=np.append([tiempo],[tiempo[i-1]+dt],axis=0)
	q=np.append([q],[qf],axis=0)
	tiempo=np.append([tiempo],[Ttol],axis=0)
	#Velocities
	qp=np.diff(q[:,0])
	for i in range(1,len(qo)):
		qp=np.append([qp],[np.diff(q[:,i])])
	Vmax=np.mean(qp[:,0])
	for i in range(1,len(qo)):
	    Vmax=np.append([Vmax],[np.mean(qp[:,i])])
	#Soft
	#q soft
	qs=qo;
	for j in range(0,len(qo)):
		q_o=qo[0,j]
		for i in range(1,len(tiempo)):
			tn=tiempo[i];
			if tn<=Tac:
				t=tn;
				a0=q_o;
				a1=0;a2=0;a3=0;
				a4=(5/(2*Tac**3))*Vmax[j];
				a5=(-3/(Tac**4))*Vmax[j];
				a6=(1/(Tac**5))*Vmax[j];
				qs[i,j]=(a6*(t**6))+(a5*(t**5))+(a4*(t**4))+(a3*(t**3))+(a2*(t**2))+(a1*t)+a0;
			elif tn>=Tac and tn<(Ttol-Tac):
				t=tn-Tac;
				b0=q_o+(Tac/2)*Vmax[j];
				b1=Vmax[j];
				qs[i,j]=b1*t+b0;
			elif tn>=(Ttol-Tac):
				t=tn-(Ttol-Tac);
				c0=(Ttol-(3/2)*Tac)*Vmax[j]+q_o;
				c1=Vmax[j];
				c2=0;c3=0;
				c4=(-5/(2*Tac**3))*Vmax[j];
				c5=(3/(Tac**4))*Vmax[j];
				c6=(-1/(Tac**5))*Vmax[j];
				qs[i,j]=(c6*(t**6))+(c5*(t**5))+(c4*(t**4))+(c3*(t**3))+(c2*(t**2))+(c1*t)+c0;
	return qs
	
