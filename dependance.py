# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 09:40:48 2024

@author: simon
"""

from scipy.stats import poisson
import matplotlib.pyplot as plt
import math

# Initialisation
C0 = 0
S0 = 0.5
E0 = 0

# Paramètres

d = 0.2 #depression du désir au cours du temps
"""
plus d est petit plus l'intensité de désir disparait lentement
si on somme C et S on obtient 0.5 c'est SMAX plus le désir diminue plus le self control augmente
"""
p = 0.2#résilience psychologique, influe sur le self controle, coeff de régéneration du self control
ne = 0
poi = 0.2
Rmax = 7
Smax = 0.8
q = 0.8 #ce que le corp de l'individu est capable d'ingérer
b = 2*d/q
h =  p*Smax
k = p*Smax/q

Tmax = 200

# Fonction V

def Vulne(t):
    psi = c[t] - s[t] - e[t]
    return max(0,min(psi,1))

# Loi de Poisson

POI = [poisson.rvs(mu=poi,size=1)[0]]

# Création des suites

c = [C0]
s = [S0]
e = [E0]
v = [Vulne(0)]
a = [q*v[0]+POI[0]*q*(1-v[0])/Rmax]

# Dynamique
for j in range(1,Tmax):
    poi +=0.001
    POI = poisson.rvs(mu=min(poi,0.5),size=1)[0]
    c.append((1-d)*c[j-1]+b*a[j-1]*min(1,1-c[j-1]))
    s.append(s[j-1] + p*max(0,Smax-s[j-1]) - h*c[j-1] - k*a[j-1])
    e.append((e[j-1])-3*ne)
    v.append(Vulne(j))
    a.append(q*v[j]+POI*q*(1-v[j])/Rmax)
   

# Calcul du Taux de Vulnérabilité
taux_vulnerabilite = [0]
for i in range(1,Tmax):
    ind = 0
    for l in range(max(i-100,0),i):
        if (v[l]>=0.85):
            ind+=1
    taux_vulnerabilite.append(ind/min(i,100))

# Tracer le graphique
plt.figure(figsize=(10, 5))
plt.plot(range(Tmax), c, label='C (intensité de désir)', color='blue')
plt.plot(range(Tmax), s, label='S (intesité de self control)', color='green')
plt.plot(range(Tmax), v, label='V (vulnérabilité)', color='red')
plt.plot(range(Tmax), a, label='A (fréquence de consommation)', color='cyan')


plt.legend()
plt.title('Evolution de C, S, A et V en fonction du temps')
plt.xlabel('Temps')
plt.ylabel('Valeurs')
plt.grid(True)
plt.show()