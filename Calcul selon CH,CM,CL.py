
import numpy as np
from datetime import (datetime,date)
from matplotlib.dates import (datestr2num, num2date)
import matplotlib.pyplot as plt
import math
import tkinter.filedialog
import tkinter.messagebox
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'qt5')
fichier_ouv = tkinter.filedialog.askopenfilename(title = " fichier " )

M = np.loadtxt(fichier_ouv, skiprows=4)

texp = np.array(M[:, 0])
KDexp = np.array(M[:, 1])
KUexp = np.array(M[:, 2])
# Lexp = np.array(M[:,3])
# Qexp = np.array(M[:, 4])
LDexp = np.array(M[:, 3])
LUexp = np.array(M[:, 4])
Qexp = np.array(M[:, 5])


# Boucle pour tester les valeurs selon les variables
#-------------------------------------INFO----------------------
# Mizuho Station, Antarctica (70.4157°N 44,1645°E) 13/11/1979
# Matador, Saskatchewan 30/07/1971 (50.800°N -107.951°W)
# Lake Ontario, Grimsby, Ontario 28/08/1969 (43.200°N -79.550°W)
# Rothamsted, UK 23/07/1963 (51.809°N -0.355°W)
# Cedar River Washington 10/08/1972 (47.473°N -122.162°W)
choix = 1
nom = "Cedar River Washington 10/08/1972 (47.473°N -122.162°W)"

annee = 1972
mois = 8
jour = 10

Latitude = 47.473
Longitude = -122.162


resultCH, resultCM, resultCL = np.zeros(11), np.zeros(11), np.zeros(11)
resultCH_2, resultCM_2, resultCL_2 = np.zeros(11), np.zeros(11), np.zeros(11)

I = np.where(KDexp==max(KDexp)) # Cherche l'indice de 12h
A = -KUexp[I[0]]/KDexp[I[0]] #Calcul de l'albedo à 12h locale à partir des données exp
# moins empiriques !                                  
S0 = 1370 # Constantes solaires dans l'espace
Date= date(int(annee), int(mois), int(jour)) # Format des dates
time = date(int(annee), int(mois), int(jour)).isoformat() # Autre Format Date
timenum = datestr2num(datetime.strptime(time, '%Y-%m-%d').strftime('%d/%m/%Y'))
# Calcul du temps numérique, nombre de jours depuis le 01/01/1970

lat = math.radians(Latitude) # latitude en radians !
long = math.radians(Longitude) # longitude en radians !

Offset = long/(2*np.pi/24) # Offset représentant le décalage temporel entre 
# le temps universel UTC et le temps local d'une position définie !

for malek in range(0,11,1):
    #-----------------------------Paramètres du modèle--------------------------
    CH = malek/10 # cloud cover (0-1) for high level clouds
    CM = 0 # cloud cover (0-1) for middle level clouds
    CL = 0 #  cloud cover (0-1) for low level clouds
    compte = -1 # Ca servira à créer une liste pour les données
    w= [0]*(2*24*60)
    d= [0]*(2*24*60) # Initialisation des listes ou tableaux de données
    h= [0]*(2*24*60)
    UTC= [0]*(2*24*60)
    Local = [0]*(2*24*60)
    N = Date.toordinal() - date(Date.year, 1, 1).toordinal() + 1 # Nombre de jour
    # passé depuis le 1er janvier d'une année.
    
    #-------------------------------Calcul du modèle-----------------------------
    for t in np.arange(timenum,timenum+2,(1/(24*60))): 
        compte = compte + 1
        UTC[compte]= (t-timenum)*24
        Local[compte] = (t-timenum)*24+Offset
        w[compte]=((np.pi*UTC[compte])/12) + long
        d=0.409*np.sin((2*np.pi*(N-173))/365)
        h[compte]=np.arcsin((np.sin(lat)*np.sin(d))-(np.cos(lat)*np.cos(d)*np.cos(w[compte])))
    T = [0]*len(h)
    KD = [0]*len(h)
    KU = [0]*len(h)
    L = [0]*len(h)
    Net = [0]*len(h)
    for i in range(0,len(h)):
        if h[i]>=0:
            T[i] = (0.6+(0.2*np.sin(h[i])))*(1-(0.4*float(CH)))*(1-(0.7*float(CM)))*(1-(0.4*float(CL)))
            KD[i] = S0*T[i]*np.sin(h[i])
            KU[i] = -float(A)*KD[i]
            L[i] = -97.28*(1-(0.1*float(CH))-(0.3*float(CM))-(0.6*float(CL)))
            Net[i] = L[i] + KD[i] + KU[i]
    P = np.where(L==min(L))
    resultCH[malek]= L[0]
    P = np.where(Net==max(Net))
    resultCH_2[malek]= Net[P[0][0]]


for malek in range(0,11,1):
    #-----------------------------Paramètres du modèle--------------------------
    CH = 0 # cloud cover (0-1) for high level clouds
    CM = malek/10 # cloud cover (0-1) for middle level clouds
    CL = 0 #  cloud cover (0-1) for low level clouds
    A = -KUexp[I[0]]/KDexp[I[0]] #Calcul de l'albedo à 12h locale à partir des données exp
    # moins empiriques !                                  
    S0 = 1370 # Constantes solaires dans l'espace
    Date= date(int(annee), int(mois), int(jour)) # Format des dates
    time = date(int(annee), int(mois), int(jour)).isoformat() # Autre Format Date
    timenum = datestr2num(datetime.strptime(time, '%Y-%m-%d').strftime('%d/%m/%Y'))
    # Calcul du temps numérique, nombre de jours depuis le 01/01/1970

    lat = math.radians(Latitude) # latitude en radians !
    long = math.radians(Longitude) # longitude en radians !

    Offset = long/(2*np.pi/24) # Offset représentant le décalage temporel entre 
    # le temps universel UTC et le temps local d'une position définie !
    compte = -1 # Ca servira à créer une liste pour les données
    w= [0]*(2*24*60)
    d= [0]*(2*24*60) # Initialisation des listes ou tableaux de données
    h= [0]*(2*24*60)
    UTC= [0]*(2*24*60)
    Local = [0]*(2*24*60)
    N = Date.toordinal() - date(Date.year, 1, 1).toordinal() + 1 # Nombre de jour
    # passé depuis le 1er janvier d'une année.
    
    #-------------------------------Calcul du modèle-----------------------------
    for t in np.arange(timenum,timenum+2,(1/(24*60))): 
        compte = compte + 1
        UTC[compte]= (t-timenum)*24
        Local[compte] = (t-timenum)*24+Offset
        w[compte]=((np.pi*UTC[compte])/12) + long
        d=0.409*np.sin((2*np.pi*(N-173))/365)
        h[compte]=np.arcsin((np.sin(lat)*np.sin(d))-(np.cos(lat)*np.cos(d)*np.cos(w[compte])))
    T = [0]*len(h)
    KD = [0]*len(h)
    KU = [0]*len(h)
    L = [0]*len(h)
    Net = [0]*len(h)
    for i in range(0,len(h)):
        if h[i]>=0:
            T[i] = (0.6+(0.2*np.sin(h[i])))*(1-(0.4*float(CH)))*(1-(0.7*float(CM)))*(1-(0.4*float(CL)))
            KD[i] = S0*T[i]*np.sin(h[i])
            KU[i] = -float(A)*KD[i]
            L[i] = -97.28*(1-(0.1*float(CH))-(0.3*float(CM))-(0.6*float(CL)))
            Net[i] = L[i] + KD[i] + KU[i]
    P = np.where(L==min(L))        
    resultCM[malek]= L[0]
    P = np.where(Net==max(Net))
    resultCM_2[malek]= Net[P[0][0]]


for malek in range(0,11,1):
    #-----------------------------Paramètres du modèle--------------------------
    CH = 0 # cloud cover (0-1) for high level clouds
    CM = 0 # cloud cover (0-1) for middle level clouds
    CL = malek/10 #  cloud cover (0-1) for low level clouds
    A = -KUexp[I[0]]/KDexp[I[0]] #Calcul de l'albedo à 12h locale à partir des données exp
    # moins empiriques !                                  
    S0 = 1370 # Constantes solaires dans l'espace
    Date= date(int(annee), int(mois), int(jour)) # Format des dates
    time = date(int(annee), int(mois), int(jour)).isoformat() # Autre Format Date
    timenum = datestr2num(datetime.strptime(time, '%Y-%m-%d').strftime('%d/%m/%Y'))
    # Calcul du temps numérique, nombre de jours depuis le 01/01/1970

    lat = math.radians(Latitude) # latitude en radians !
    long = math.radians(Longitude) # longitude en radians !

    Offset = long/(2*np.pi/24) # Offset représentant le décalage temporel entre 
    # le temps universel UTC et le temps local d'une position définie !
    compte = -1 # Ca servira à créer une liste pour les données
    w= [0]*(2*24*60)
    d= [0]*(2*24*60) # Initialisation des listes ou tableaux de données
    h= [0]*(2*24*60)
    UTC= [0]*(2*24*60)
    Local = [0]*(2*24*60)
    N = Date.toordinal() - date(Date.year, 1, 1).toordinal() + 1 # Nombre de jour
    # passé depuis le 1er janvier d'une année.
    
    #-------------------------------Calcul du modèle-----------------------------
    for t in np.arange(timenum,timenum+2,(1/(24*60))): 
        compte = compte + 1
        UTC[compte]= (t-timenum)*24
        Local[compte] = (t-timenum)*24+Offset
        w[compte]=((np.pi*UTC[compte])/12) + long
        d=0.409*np.sin((2*np.pi*(N-173))/365)
        h[compte]=np.arcsin((np.sin(lat)*np.sin(d))-(np.cos(lat)*np.cos(d)*np.cos(w[compte])))
    T = [0]*len(h)
    KD = [0]*len(h)
    KU = [0]*len(h)
    L = [0]*len(h)
    Net = [0]*len(h)
    for i in range(0,len(h)):
        if h[i]>=0:
            T[i] = (0.6+(0.2*np.sin(h[i])))*(1-(0.4*float(CH)))*(1-(0.7*float(CM)))*(1-(0.4*float(CL)))
            KD[i] = S0*T[i]*np.sin(h[i])
            KU[i] = -float(A)*KD[i]
            L[i] = -97.28*(1-(0.1*float(CH))-(0.3*float(CM))-(0.6*float(CL)))
            Net[i] = L[i] + KD[i] + KU[i]
    P = np.where(L==min(L))       
    resultCL[malek]= L[0]
    P = np.where(Net==max(Net))
    resultCL_2[malek]= Net[P[0][0]]
    
x = np.arange(0,11,1)/10
print(x)
plt.plot(x,resultCH)
plt.plot(x,resultCM)
plt.plot(x,resultCL)
plt.xlabel("cloud cover",fontsize = 15)
plt.ylabel("L net W/m²",fontsize = 15)
plt.legend(["high level clouds","medium level clouds","low level clouds"],fontsize = 8)
plt.title(f"L net flux depending on the cloud cover (0-1) \n {nom} \n midday")
plt.show()
plt.figure()
plt.plot(x,resultCH_2)
plt.plot(x,resultCM_2)
plt.plot(x,resultCL_2)
plt.xlabel("cloud cover",fontsize = 15)
plt.ylabel("Net W/m²",fontsize = 15)
plt.legend(["high level clouds","medium level clouds","low level clouds"],fontsize = 8)
plt.title(f"Net flux depending on the cloud cover (0-1) \n {nom} \n midday")
plt.show()
