import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#---------------------------------Initialisation------------------------------

Ed = np.zeros([10]) # Radiation descendant (down)
Eu = np.zeros([10]) # Radiation ascendant (up)
eps = np.zeros([10])
T=np.zeros([100000,10])
dT= np.zeros([10])
temps = np.zeros([100000])
Tab =[0]*10
H=2
sig = 5.67e-8
H=2
a=0.3
E = 342
ES = E*(1-a)
def eps(n):
    eps = np.exp(-n/H)
    return eps
C = 10e7
N = 10
dt=10000
# somme = 1
# TN = (ES/(sig*(2-eps(N))))**(1/4)
# for i in range(0,N+1):
#     if i<N : 
#         somme = somme + (eps(i+1)/(2-eps(i+1)))
#         T0[i]=((2-eps(N))*((1/(2-eps(i)))+somme)*(TN)**4)**(1/4)
#         Tab[i]=i
# plt.plot(T0,Tab)

#---------------------------------Calcul du model---------------------------

for t in range (0,100000): # boucle sur un temps t fictif, faut lui multiplier dt.
    temps[t] = (t*dt)/(365*24*3600) # Temps en année 
    for n1 in range(0,N):
        if t == 0:
            T[t,n1]=200 # Température initiale
        else:
            T[t,n1]=T[t-1,n1]+dT[n1]
        if n1 == 0:
            Eu[n1]=eps(n1)*sig*(T[t,n1])**4
        else :
            Eu[n1]= (eps(n1)*sig*(T[t,n1])**4)+(1-eps(n1))*Eu[n1-1]
    for n2 in range(N-1,-1,-1):
        if n2 == (N-1):
            Ed[n2]=eps(n2)*sig*(T[t,n2])**4
        else:
            Ed[n2]=(eps(n2)*sig*(T[t,n2])**4)+(1-eps(n2))*Ed[n2+1]
    for n in range(0,N):
        if n>0 and n<N-1:
            dT[n] = ((Ed[n+1]+Eu[n-1]-Eu[n]-Ed[n])*dt)/C
        if n==0:
            dT[n] = ((ES-Eu[n]+Ed[n+1])*dt)/C
        if n==N:
            dT[n] = ((Eu[n-1]-Eu[n]-Ed[n])*dt)/C
            
#--------------------------------Plot----------------------------------------

plt.plot(temps,T[:,0],label='n=1')
plt.plot(temps,T[:,1],label='n=2')
plt.plot(temps,T[:,2],label='n=3')
plt.plot(temps,T[:,3],label='n=4')
plt.plot(temps,T[:,4],label='n=5')
plt.plot(temps,T[:,5],label='n=6')
plt.plot(temps,T[:,6],label='n=7')
plt.plot(temps,T[:,7],label='n=8')
plt.plot(temps,T[:,8],label='n=9')
plt.plot(temps,T[:,9],label='n=10')
plt.legend()
plt.xlabel('time(year)')
plt.ylabel('T(K)')
plt.show()
