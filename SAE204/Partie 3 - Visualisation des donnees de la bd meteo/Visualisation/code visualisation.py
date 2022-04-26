# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 19:15:20 2022

@author: Nils Saadi
"""

import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("donnees-synop-essentielles-omm.csv")

groupement_par_mois = data.groupby("mois_de_l_annee")
liste_mois = []
for i in range (len(groupement_par_mois)):
    liste_mois.append(i+1)


groupement_par_region = data.groupby("region (name)")

paca = data.loc[data["region (name)"]=="Provence-Alpes-Côte d'Azur"]
paca_groupement_par_mois = paca.groupby("mois_de_l_annee")
paca_groupement_par_departement = paca.groupby("department (name)")


bouche_de_rhone = data.loc[data["department (name)"]=="Bouches-du-Rhône"]
bouche_de_rhone_groupement_par_mois = bouche_de_rhone.groupby("mois_de_l_annee")

direction_vent_bouche_de_rhone= bouche_de_rhone.groupby("Direction du vent moyen 10 mn")
moyenne_bouche_de_rhone_groupement_par_mois = bouche_de_rhone_groupement_par_mois.mean()


mayotte = data.loc[data["department (name)"]=="Mayotte"]
mayotte_groupement_par_mois = mayotte.groupby("mois_de_l_annee")

direction_vent_mayotte= mayotte.groupby("Direction du vent moyen 10 mn")
moyenne_mayotte_groupement_par_mois = mayotte_groupement_par_mois.mean()

alpes_aritimes = data.loc[data["department (name)"]=="Alpes-Maritimes"]
alpes_aritimes_groupement_par_mois = alpes_aritimes.groupby("mois_de_l_annee")

direction_vent_alpes_aritimes= alpes_aritimes.groupby("Direction du vent moyen 10 mn")
moyenne_alpes_aritimes_groupement_par_mois = alpes_aritimes_groupement_par_mois.mean()

"""
Stat a l'echelle de la France
"""
#la Temperature
data["Température (°C)"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des tempérarure en °C de toute la France")
plt.show()

print("Description de la température en France")
print(data["Température (°C)"].describe())
print('\n')
print('\n')

#La pluie
data["Précipitations dans les 12 dernières heures"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des tempérarure en °C de toute la France")
plt.show()

print("Description des précipitations dans les 12 dernières heures avant le relever en France")
print(data["Précipitations dans les 12 dernières heures"].describe())
print('\n')
print('\n')


plt.plot(liste_mois, groupement_par_mois["Précipitations dans les 12 dernières heures"].count())
plt.title("Courbe des précipitations totale par mois en mm en France")
plt.show()

#Le vent
data["Vitesse du vent moyen 10 mn"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite de la vitesse du vent sur toute la France")
plt.show()

print("Description de la vitesse du vent moyen puis des rafale de vent sur la France")
print(data["Vitesse du vent moyen 10 mn"].describe())
print('\n')
print('\n')
print(data["Rafale sur les 10 dernières minutes"].describe())
print('\n')
print('\n')


#Graph en fonction du mois
plt.plot(liste_mois, groupement_par_mois["Température (°C)"].mean())
plt.title("Courbe de la temperature en fonction du mois")
plt.show()

"""
Stat a l'echelle des regions
"""

groupement_par_region["Précipitations dans les 12 dernières heures"].count().plot.pie(autopct = lambda z: str(round(z, 2)) + '%', pctdistance = 0.8)
plt.title("Repartion des précipitation par region en mm")
plt.show()

groupement_par_region["Température (°C)"].mean().plot.bar(width=0.8,edgecolor='black')
plt.title("Moyenne des temprérature en °C par région")
plt.show()

groupement_par_region["Vitesse du vent moyen 10 mn"].mean().plot.bar(width=0.5,edgecolor='black')
plt.title("Vitesse moyenne du vent en m/s par région")
plt.show()


"""
Regardons plus en detail la region PACA
"""

paca["Température (°C)"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des tempérarure en °C dans la region PACA")
plt.show()

print("Description de la température dans la région PACA")
print(paca["Température (°C)"].describe())
print('\n')
print('\n')

plt.plot(liste_mois, paca_groupement_par_mois["Température (°C)"].mean())
plt.title("Courbe de la temperature en °C en fonction du mois dans la region PACA")
plt.show()

paca_groupement_par_departement["Température (°C)"].mean().plot.bar(width=0.8,edgecolor='black')
plt.title("Moyenne des temprérature en °C dans le region PACA")
plt.show()



#La pluie
paca["Précipitations dans les 12 dernières heures"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des précipitation en mm dans la region PACA")
plt.show()

print("Description des précipitations en mm dans les 12 dernières heures avant le relever dans la region PACA")
print(paca["Précipitations dans les 12 dernières heures"].describe())
print('\n')
print('\n')

paca_groupement_par_departement["Précipitations dans les 12 dernières heures"].mean().plot.bar(width=0.8,edgecolor='black')
plt.title("Moyenne des precipitation en mm dans le region PACA")
plt.show()

#Le vent

paca["Vitesse du vent moyen 10 mn"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite de la vitesse du vent en m/s dans la region PACA")
plt.show()

print("Description de la vitesse du vent moyen puis des rafale de vent sur la region PACA")
print(paca["Vitesse du vent moyen 10 mn"].describe())
print('\n')
print('\n')
print(paca["Rafale sur les 10 dernières minutes"].describe())
print('\n')
print('\n')





"""
Regardons plus en detail dans le departement des bouche du rhone
"""
#temperature

bouche_de_rhone["Température (°C)"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des tempérarure en °C dans les Bouches-du-Rhône")
plt.show()


plt.plot(liste_mois, bouche_de_rhone_groupement_par_mois["Température (°C)"].mean())
plt.title("Courbe de la temperature en fonction du mois dans les Bouches-du-Rhône en °C")
plt.show()

print("Description de la température dans les Bouches-du-Rhône ")
print(bouche_de_rhone["Température (°C)"].describe())
print('\n')
print('\n')

#La pluie
bouche_de_rhone["Précipitations dans les 12 dernières heures"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des précipitations en mm dans les 12 dernières heures dans les Bouches-du-Rhône")
plt.show()


print("Description des précipitations en mm dans les 12 dernières heures avant le relever dans les Bouches-du-Rhône")
print(bouche_de_rhone["Précipitations dans les 12 dernières heures"].describe())
print('\n')
print('\n')

bouche_de_rhone_groupement_par_mois["Précipitations dans les 12 dernières heures"].count().plot.pie(autopct = lambda z: str(round(z, 2)) + '%', pctdistance = 0.6)
plt.title("Repartion des précipitation en mm dans les Bouches-du-Rhône par mois")
plt.show()

plt.plot(liste_mois, bouche_de_rhone_groupement_par_mois["Précipitations dans les 12 dernières heures"].count())
plt.title("Courbe des précipitations totale par mois en mm dans les Bouches-du-Rhône")
plt.show()

plt.plot(liste_mois, bouche_de_rhone_groupement_par_mois["Précipitations dans les 12 dernières heures"].mean())
plt.title("Courbe des précipitations moy par mois en mm dans les Bouches-du-Rhône")
plt.show()



#Le vent
bouche_de_rhone["Vitesse du vent moyen 10 mn"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite de la vitesse du vent en m/s dans les Bouches-du-Rhône")
plt.show()

bouche_de_rhone["Rafale sur les 10 dernières minutes"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des rafales de vent en m/s dans les Bouches-du-Rhône")
plt.show()

plt.scatter(bouche_de_rhone["Direction du vent moyen 10 mn"],bouche_de_rhone["Vitesse du vent moyen 10 mn"])
plt.title("nuage de point de la vitesse du vent en m/s en fonction de la direction")
plt.show()


moyenne_bouche_de_rhone_groupement_par_mois.plot.bar(y=["Température (°C)","Précipitations dans les 12 dernières heures","Vitesse du vent moyen 10 mn"], secondary_y = "Température (°C)",legend = None)
plt.title("Diagramme de la temperature en °C (bleu-droite), precipitation en mm (orange-gauche) et vitesse du vent en m/s(vert-gauche) en fonction du mois dans les Bouches-du-Rhône")
plt.show()

print("Description de la vitesse du vent moyen puis des rafale de vent sur la France")
print(bouche_de_rhone["Vitesse du vent moyen 10 mn"].describe())
print('\n')
print('\n')
print(bouche_de_rhone["Rafale sur les 10 dernières minutes"].describe())
print('\n')
print('\n')


direction_vent_bouche_de_rhone["Vitesse du vent moyen 10 mn"].mean().plot.bar(width=0.8,edgecolor='black')
plt.title("Moyenne de la vitesse du vent en m/s dans les Bouches-du-Rhône")
plt.show()

"""
Mayotte
"""

mayotte["Température (°C)"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des tempérarure en °C à Mayotte")
plt.show()


plt.plot(liste_mois, mayotte_groupement_par_mois["Température (°C)"].mean())
plt.title("Courbe de la temperature en fonction du mois à Mayotte en °C")
plt.show()

print("Description de la température às Mayotte ")
print(mayotte["Température (°C)"].describe())
print('\n')
print('\n')

#La pluie
mayotte["Précipitations dans les 12 dernières heures"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des précipitations en mm dans les 12 dernières heures à Mayotte")
plt.show()


print("Description des précipitations en mm dans les 12 dernières heures avant le relever à Mayotte")
print(mayotte["Précipitations dans les 12 dernières heures"].describe())
print('\n')
print('\n')

mayotte_groupement_par_mois["Précipitations dans les 12 dernières heures"].count().plot.pie(autopct = lambda z: str(round(z, 2)) + '%', pctdistance = 0.6)
plt.title("Repartion des précipitation en mm à Mayotte par mois")
plt.show()

plt.plot(liste_mois, mayotte_groupement_par_mois["Précipitations dans les 12 dernières heures"].count())
plt.title("Courbe des précipitations totale par mois en mm à Mayotte")
plt.show()

plt.plot(liste_mois, mayotte_groupement_par_mois["Précipitations dans les 12 dernières heures"].mean())
plt.title("Courbe des précipitations moy par mois en mm à Mayotte")
plt.show()



#Le vent
mayotte["Vitesse du vent moyen 10 mn"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite de la vitesse du vent en m/s à Mayotte")
plt.show()

mayotte["Rafale sur les 10 dernières minutes"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des rafales de vent en m/s à Mayotte")
plt.show()

plt.scatter(mayotte["Direction du vent moyen 10 mn"],mayotte["Vitesse du vent moyen 10 mn"])
plt.title("nuage de point de la vitesse du vent en m/s en fonction de la direction")
plt.show()


moyenne_mayotte_groupement_par_mois.plot.bar(y=["Température (°C)","Précipitations dans les 12 dernières heures","Vitesse du vent moyen 10 mn"], secondary_y = "Température (°C)",legend = None)
plt.title("Diagramme de la temperature en °C (bleu-droite), precipitation en mm (orange-gauche) et vitesse du vent en m/s(vert-gauche) en fonction du mois à Mayotte")
plt.show()

print("Description de la vitesse du vent moyen puis des rafale de vent à Mayotte")
print(mayotte["Vitesse du vent moyen 10 mn"].describe())
print('\n')
print('\n')
print(mayotte["Rafale sur les 10 dernières minutes"].describe())
print('\n')
print('\n')


direction_vent_mayotte["Vitesse du vent moyen 10 mn"].mean().plot.bar(width=0.8,edgecolor='black')
plt.title("Moyenne de la vitesse du vent en m/s à Mayotte")
plt.show()

"""
Alpes-Maritimes
"""

alpes_aritimes["Température (°C)"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des tempérarure en °C dans les Alpes-Maritimes")
plt.show()


plt.plot(liste_mois, alpes_aritimes_groupement_par_mois["Température (°C)"].mean())
plt.title("Courbe de la temperature en fonction du mois dans les Alpes-Maritimes en °C")
plt.show()

print("Description de la température dans les Alpes-Maritimes ")
print(alpes_aritimes["Température (°C)"].describe())
print('\n')
print('\n')

#La pluie
alpes_aritimes["Précipitations dans les 12 dernières heures"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des précipitations en mm dans les 12 dernières heures dans les Alpes-Maritimes")
plt.show()


print("Description des précipitations en mm dans les 12 dernières heures avant le relever dans les Alpes-Maritimes")
print(alpes_aritimes["Précipitations dans les 12 dernières heures"].describe())
print('\n')
print('\n')

alpes_aritimes_groupement_par_mois["Précipitations dans les 12 dernières heures"].count().plot.pie(autopct = lambda z: str(round(z, 2)) + '%', pctdistance = 0.6)
plt.title("Repartion des précipitation en mm dans les Alpes-Maritimes par mois")
plt.show()

plt.plot(liste_mois, alpes_aritimes_groupement_par_mois["Précipitations dans les 12 dernières heures"].count())
plt.title("Courbe des précipitations totale par mois en mm dans les Alpes-Maritimes")
plt.show()

plt.plot(liste_mois, alpes_aritimes_groupement_par_mois["Précipitations dans les 12 dernières heures"].mean())
plt.title("Courbe des précipitations moy par mois en mm dans les Alpes-Maritimes")
plt.show()



#Le vent
alpes_aritimes["Vitesse du vent moyen 10 mn"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite de la vitesse du vent en m/s dans les Alpes-Maritimes")
plt.show()

alpes_aritimes["Rafale sur les 10 dernières minutes"].plot.box(whis=[0,100],vert=False)
plt.title("Diagramme en boite des rafales de vent en m/s dans les Alpes-Maritimes")
plt.show()

plt.scatter(alpes_aritimes["Direction du vent moyen 10 mn"],alpes_aritimes["Vitesse du vent moyen 10 mn"])
plt.title("nuage de point de la vitesse du vent en m/s en fonction de la direction")
plt.show()


moyenne_alpes_aritimes_groupement_par_mois.plot.bar(y=["Température (°C)","Précipitations dans les 12 dernières heures","Vitesse du vent moyen 10 mn"], secondary_y = "Température (°C)",legend = None)
plt.title("Diagramme de la temperature en °C (bleu-droite), precipitation en mm (orange-gauche) et vitesse du vent en m/s(vert-gauche) en fonction du mois dans les Alpes-Maritimes")
plt.show()

print("Description de la vitesse du vent moyen puis des rafale de vent dans les Alpes-Maritimes")
print(alpes_aritimes["Vitesse du vent moyen 10 mn"].describe())
print('\n')
print('\n')
print(alpes_aritimes["Rafale sur les 10 dernières minutes"].describe())
print('\n')
print('\n')


direction_vent_alpes_aritimes["Vitesse du vent moyen 10 mn"].mean().plot.bar(width=0.8,edgecolor='black')
plt.title("Moyenne de la vitesse du vent en m/s dans les Alpes-Maritimes")
plt.show()



