import numpy as np
import matplotlib.pyplot as plt
import tkinter.filedialog
import tkinter.messagebox
#---------------------------------Initialisation------------------------------

Ed = np.zeros([10]) # Radiation descendant (down)
Eu = np.zeros([10]) # Radiation ascendant (up)
eps = np.zeros([10])
T=np.zeros([100000,10])
dT= np.zeros([10])
temps = np.zeros([100000])
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
dt=100000
#T0=300
#-----------------------------Modèle stationnaire inhomogène-----------------
fichier_ouv = tkinter.filedialog.askopenfilename(title = " fichier " )

Tmesure = np.loadtxt(fichier_ouv,skiprows=1)

Teq = np.zeros([11])
Tab =[0]*11
TN = (ES/(sig*(2-eps(N))))**(1/4)
for i in range(0,N+1):
    somme = 0
    n = i+1
    for j in range(n,N+1): 
            somme = somme + (eps(j+1)/(2-eps(1+j))) 
    Teq[i]=((2-eps(N))*((1/(2-eps(i)))+somme)*(TN)**4)**(1/4)
    Tab[i]=i
plt.title("Température à l'équilibre de chaque couche n",fontsize=30)
plt.tick_params(axis='x', labelsize=20)
plt.tick_params(axis='y', labelsize=20)
plt.xlabel('Temperature T(K)',fontsize = 22)
plt.ylabel('Couche n',fontsize = 22)
plt.plot(Teq,Tab,label="modèle")
plt.plot(Tmesure[:,1],Tmesure[:,0],label="mesure")
plt.legend(fontsize = 19)
#---------------------------------Calcul du model non stationnaire---------------------------

# for t in range (0,100000): # boucle sur un temps t fictif, faut lui multiplier dt.
#     temps[t] = (t*dt)/(365*24*3600) # Temps en année 
#     for n1 in range(0,N):
#         if t == 0:
#             T[t,n1]=T0 # Température initiale
#         else:
#             T[t,n1]=T[t-1,n1]+dT[n1]
#         if n1 == 0:
#             Eu[n1]=eps(n1)*sig*(T[t,n1])**4
#         else :
#             Eu[n1]= (eps(n1)*sig*(T[t,n1])**4)+(1-eps(n1))*Eu[n1-1]
#     for n2 in range(N-1,-1,-1):
#         if n2 == (N-1):
#             Ed[n2]=eps(n2)*sig*(T[t,n2])**4
#         else:
#             Ed[n2]=(eps(n2)*sig*(T[t,n2])**4)+(1-eps(n2))*Ed[n2+1]
#     for n in range(0,N):
#         if n>0 and n<N-1:
#             dT[n] = ((Ed[n+1]+Eu[n-1]-Eu[n]-Ed[n])*dt)/C
#         if n==0:
#             dT[n] = ((ES-Eu[n]+Ed[n+1])*dt)/C
#         if n==N:
#             dT[n] = ((Eu[n-1]-Eu[n]-Ed[n])*dt)/C
            
# #--------------------------------Plot----------------------------------------
# plt.title(f"Température initiale {T0} K",fontsize=30)
# plt.plot(temps,T[:,0],label='n=1')
# plt.plot(temps,T[:,1],label='n=2')
# plt.plot(temps,T[:,2],label='n=3')
# plt.plot(temps,T[:,3],label='n=4')
# plt.plot(temps,T[:,4],label='n=5')
# plt.plot(temps,T[:,5],label='n=6')
# plt.plot(temps,T[:,6],label='n=7')
# plt.plot(temps,T[:,7],label='n=8')
# plt.plot(temps,T[:,8],label='n=9')
# plt.plot(temps,T[:,9],label='n=10')
# plt.legend(fontsize = 19)
# plt.xlabel('time(year)',fontsize = 22)
# plt.ylabel('T(K)',fontsize = 22)
# plt.tick_params(axis='x', labelsize=20)
# plt.tick_params(axis='y', labelsize=20)
# plt.show()

