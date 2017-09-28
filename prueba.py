'''
Prueba
Programa para validar la informacion que se ha realizado en la libreria
del MURA.
Autor: Juan Cely
Fecha: Septiembre/2017
Grupo de Robots y Maquinas Inteligentes
'''
import GRMI_MUR.Arm.arm_parts as Arm_parts
import GRMI_MUR.AWS.AWS_updater as AWS_updater
import GRMI_MUR.Arm.kine as Arm_kine
import GRMI_MUR.Arm.move as arm_move
import GRMI_MUR.Simulate.arm as vrep_arm
import GRMI_MUR.Common.converter as AWS_converter
import time
import numpy as np
import matplotlib.pyplot as plt

## Creacion de puntos
x=0.6402
y=-0.0281
z=0.0839
theta=83.33
phi=-140

x1=0.1534
y1=-0.0430
z1=0.4129
theta1=30
phi1=-38.33

## Programa
# Init VREP
vrep_arm.init('192.168.4.111',19999)
#vrep_arm.init('192.168.0.159',19999)

# Inverse
q1,q2,q3,q4,q5=Arm_kine.inversekine(x,y,z,theta,phi)
print q1
print q2
print q3
print q4
print q5
# D-H
DH=Arm_parts.GetDH()
print DH
# DoF
num_dof=Arm_parts.GetDOF()
print num_dof
# Direct Kinematic
values=Arm_kine.directkine(q1,q2,q3,q4,q5)
print values
# Jacobian
j=Arm_kine.jacobiana_matrix(q1,q2,q3,q4,q5)
print j
# Path
Ttol=20
Tac=4.5
n=30
qs,qp,qpp,tiempo=arm_move.planner_616(x,y,z,theta,phi,Ttol,Tac,n)

plt.figure()
plt.plot(tiempo,qp)
plt.legend(('q1','q2','q3','q4','q5'))
plt.show()

