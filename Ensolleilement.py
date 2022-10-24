import numpy as np
from datetime import (datetime,date)
from matplotlib.dates import (datestr2num, num2date)
import matplotlib.pyplot as plt
import math
import tkinter.filedialog
import tkinter.messagebox

#-------------------------------------INFO----------------------
# UK 23/07/1963 ; long = -0.355°W ; lat = 51.809°N 
# Matador 30/07/1971 ; long = -107.951° ; lat = 50.800° 
# Lake Ontario, Grimsby, Ontario 28/08/1969 ; lat = 43.200°N ; long = -79.561630
# Mizuho Station, Antarctica 13/11/1979 ; lat = 70.698°S ; long = 44.332°E UTC+3
# Cedar River. Washington 10/08/1972 ; lat = 47.473°N ; long = -122.162°W

annee = 1969
mois = 8
jour = 28

Latitude = 43.200
Longitude = -79.561630

Offset = -5
# Offset, décalage UTC, négatif si long négatif.
#----------------------------Ouverture des données exp-----------------------

fichier_ouv = tkinter.filedialog.askopenfilename(title = " fichier " )

M = np.loadtxt(fichier_ouv, skiprows=4)

texp = np.array(M[:, 0])
KDexp = np.array(M[:, 1])
KUexp = np.array(M[:, 2])
#Lexp = np.array(M[:,3])
#Qexp = np.array(M[:, 4])
LDexp = np.array(M[:, 3])
LUexp = np.array(M[:, 4])
Qexp = np.array(M[:, 5])

#-----------------------------Paramètres du modèle--------------------------
CH =0.1 # cloud cover (0-1) for high level clouds
CM = 0.01 # cloud cover (0-1) for middle level clouds
CL = 0.01 #  cloud cover (0-1) for low level clouds
I = np.where(texp==12) # Cherche l'indice de 12h
A = -KUexp[I[0]]/KDexp[I[0]] #Calcul de l'albedo à 12h loacle à partir des données exp
# moins empiriques !                                  
S0 = 1370 # Constantes solaires dans l'espace
Date= date(int(annee), int(mois), int(jour)) # Format des dates
time = date(int(annee), int(mois), int(jour)).isoformat() # Autre Format Date
timenum = datestr2num(datetime.strptime(time, '%Y-%m-%d').strftime('%d/%m/%Y'))
# Calcul du temps numérique, nombre de jours depuis le 01/01/1970

lat = math.radians(Latitude) # latitude en radians !
long = math.radians(Longitude) # longitude en radians !

#Offset = long/(2*np.pi/24) # Offset représentant le décalage temporel entre 
# le temps universel UTC et le temps local d'une position définit !
compte = -1 # Ca servira à créer une liste pour les données
w= [0]*(3*24*60)
d= [0]*(3*24*60) # Initialisation des listes ou tableaux de données
h= [0]*(3*24*60)
UTC= [0]*(3*24*60)
Local = [0]*(3*24*60)
dh = [0]*(3*24*60)
N = Date.toordinal() - date(Date.year, 1, 1).toordinal() + 1 # Nombre de jour
# passé depuis le 1er janvier d'une année.

#-------------------------------Calcul du modèle-----------------------------

for t in np.arange(timenum-1,timenum+2,(1/(24*60))): 
    compte = compte + 1
    UTC[compte]= (t-timenum)*24
    Local[compte] = (t-timenum)*24+Offset
    
    w[compte]=((np.pi*(UTC[compte]))/12) + long
    d=0.409*np.sin((2*np.pi*(N-81))/365)
    h[compte]=np.arcsin((np.sin(lat)*np.sin(d))-(np.cos(lat)*np.cos(d)*np.cos(w[compte])))
    dh[compte] = math.degrees(h[compte])
T = [0]*len(h)
KD = [0]*len(h)
KU = [0]*len(h)
L = [0]*len(h)
Net = [0]*len(h)
for i in range(0,len(h)):
    if (h[i]>=0):
        T[i] = (0.6+(0.2*np.sin(h[i])))*(1-(0.4*float(CH)))*(1-(0.7*float(CM)))*(1-(0.4*float(CL)))
        KD[i] = S0*T[i]*np.sin(h[i])
        KU[i] = -float(A)*KD[i]
        L[i] = -97.28*(1-(0.1*float(CH))-(0.3*float(CM))-(0.6*float(CL)))
        Net[i] = L[i] + KD[i] + KU[i]
        

#----------------------------------Affichage----------------------------------

plt.plot(Local,KD)
plt.plot(Local,KU)
plt.plot(Local,L)
plt.plot(Local,Net)
plt.xlabel("Temps",fontsize = 15)
plt.ylabel("W/m²",fontsize = 15)
# plt.xlabel("Temps(h)")
# plt.ylabel("Angle(°)")
# plt.plot(Local,dh)
plt.xlim(0,24)
plt.show()

plt.plot(texp,KDexp,'--')
plt.plot(texp,KUexp,'--')
#plt.plot(texp,Lexp)
plt.plot(texp,LUexp,'--')
plt.plot(texp,LDexp,'--')
plt.plot(texp,Qexp,'--')
plt.grid()
plt.legend(["KD","KU","L","Net","KDexp","KUexp","Lexp","Netexp"],fontsize = 15)
plt.show()
