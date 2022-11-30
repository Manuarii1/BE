import numpy as np
import matplotlib.pyplot as plt
def moving_average(x, w): #Fonction permmettant d'afficher la moyenne mobile sur un jeu de donné.
            return np.convolve(x, np.ones(w), 'valid') / w
    
T0= 12 # °C
Q0= 343*365*24*60*60
A=210*365*24*60*60
B=1.85*365*24*60*60
c= 3.10*10**8
d1=0.323
d2=0.015
d3=0.5
Beta=8*10**(-4)
phiecc=np.radians(290)
phiobl = np.radians(250)
lamb = 7*10**(-4)
Tecc =100000
Tobl=41000
wecc= 2*np.pi/(Tecc)
wobl = 2*np.pi/Tobl
dt = 1
temps =  np.zeros(np.shape(np.arange(0,1000000)))
T =   np.zeros(np.shape(np.arange(0,1000000)))
fecc =  np.zeros(np.shape(np.arange(0,1000000)))
fobl = np.zeros(np.shape(np.arange(0,1000000)))
Q =   np.zeros(np.shape(np.arange(0,1000000)))
a =  np.zeros(np.shape(np.arange(0,1000000)))
test =  np.zeros(np.shape(np.arange(0,1000000)))
eps = 0.021

#%%------------------------------Modèle eccentricity--------------------------
# for t in range (0,1000000):
#     rk = np.random.normal(0,1)
#     if t == 0:
#         dT=0
#         T[0]= T0
#         D=0
#     else:
#         D=1
#         T[t]= T[t-D]+dT
#     temps[t] = (t*dt)
#     a[t]= d1-(d2*np.tanh(d3*(T[t-D]-T0)))
#     fecc[t] =Beta*np.cos(wecc*(dt*t)+phiecc)
#     Q[t] = Q0*(1+fecc[t])
#     dT = (1/c)*(Q[t-D]*(1-a[t])-A-(B*T[t-D]))*dt+(eps**(1/2)*np.sqrt(dt)*rk)
#     test[t]=dT
# plt.plot(temps,T)
# t_moy = moving_average(temps,1000) 
# T_moy = moving_average(T,1000)
# plt.plot(t_moy,T_moy)
#%%---------------------------------Modèle Eccentricity+obliquity-------------
for t in range (0,1000000):
    rk = np.random.normal(0,1)
    if t == 0:
        dT=0
        T[0]= T0
        D=0
    else:
        D=1
        T[t]= T[t-D]+dT
    temps[t] = (t*dt)
    a[t]= d1-(d2*np.tanh(d3*(T[t-D]-T0)))
    fecc[t] =Beta*np.cos(wecc*(dt*t)+phiecc)
    fobl[t]= lamb*np.cos(wobl*(dt+t)+phiobl)
    Q[t] = Q0*(1+fecc[t]+fobl[t])
    dT = (1/c)*(Q[t-D]*(1-a[t])-A-(B*T[t-D]))*dt#+(eps**(1/2)*np.sqrt(dt)*rk)
    test[t]=dT
plt.plot(temps,T)
# t_moy = moving_average(temps,1000) 
# T_moy = moving_average(T,1000)
# plt.plot(t_moy,T_moy)
