# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 14:58:05 2022

@author: Nils Saadi
"""

"""
Lorsque que vous lancerez le ficheier .sql il se pourrait qu'il des eureurs mais on peut rien y faire (enfin si mais sa rendrai le programme plus lourd pour quasiment rien)
car il y a dans les TERRE AUSTRALE ANTANTRIQUE des villes qui ont le meme code postal (ou du moins le meme code dans le .json)
donc il y aura surment des erreure dans Oracle
"""


import json
import random

"""
Avant de lancer le programme si vous ne l'avez pas deja il faut telecharger les donnes dans le format Json
On peut le faire directement avec le lien ATTENTION de pas prendre une periode trop grande il faut donc mettre des flitre de date ( sur le site c'est trés intutif)
pour un ordre d'idee 1jour = environ 430 ligne dans le json = environ 4 000 tuples dans la base de donnée
"""


#Lien pour telecharcher les donnees (si on a pas deja le fichier données.json ou si on veut d'autre données)
# https://public.opendatasoft.com/explore/dataset/donnees-synop-essentielles-omm/export/?sort=date&dataChart=eyJxdWVyaWVzIjpbeyJjaGFydHMiOlt7InR5cGUiOiJjb2x1bW4iLCJmdW5jIjoiQVZHIiwieUF4aXMiOiJwaGVuc3BlMSIsInNjaWVudGlmaWNEaXNwbGF5Ijp0cnVlLCJjb2xvciI6IiNGRjUxNUEifV0sInhBeGlzIjoiZGF0ZSIsIm1heHBvaW50cyI6IiIsInRpbWVzY2FsZSI6ImRheSIsInNvcnQiOiIiLCJjb25maWciOnsiZGF0YXNldCI6ImRvbm5lZXMtc3lub3AtZXNzZW50aWVsbGVzLW9tbSIsIm9wdGlvbnMiOnsicmVmaW5lLmRhdGUiOiIyMDIyIiwic29ydCI6ImRhdGUiLCJsb2NhdGlvbiI6IjIsLTE1LjU5MjU1LDAuMDc4MzIiLCJiYXNlbWFwIjoiamF3Zy5saWdodCJ9fX1dLCJkaXNwbGF5TGVnZW5kIjp0cnVlLCJhbGlnbk1vbnRoIjp0cnVlfQ%3D%3D&location=2,-15.59255,0.07832&basemap=jawg.light


#Ouverture du fichier .sql
fSql = open("jeuDeDonnées.sql", "a")

#Ouverture du ficher json
fVille = open("données.json") #Attention mettre le nom du fichier .json que vous avez (telecharger avec le lien)
data = json.load(fVille)


#On remplace tout les carac qui pose probleme a Oracle           
def miseAuxNorme(nomLieu):
    
    nomLieu= nomLieu.upper()
    
    nomLieu = nomLieu.replace("'", "-")
    nomLieu = nomLieu.replace("Á", "A")
    nomLieu = nomLieu.replace("À", "A")
    nomLieu = nomLieu.replace("Â", "A")
    nomLieu = nomLieu.replace("Ä", "A")
    nomLieu = nomLieu.replace("Ç", "C")
    nomLieu = nomLieu.replace("É", "E")
    nomLieu = nomLieu.replace("È", "E")
    nomLieu = nomLieu.replace("Ê", "E")
    nomLieu = nomLieu.replace("Ë", "E")
    nomLieu = nomLieu.replace("Í", "I")
    nomLieu = nomLieu.replace("Ì", "I")
    nomLieu = nomLieu.replace("Î", "I")
    nomLieu = nomLieu.replace("Ï", "I")
    nomLieu = nomLieu.replace("Ñ", "N")
    nomLieu = nomLieu.replace("Ó", "O")
    nomLieu = nomLieu.replace("Ò", "O")
    nomLieu = nomLieu.replace("Ô", "O")
    nomLieu = nomLieu.replace("Ö", "O")
    nomLieu = nomLieu.replace("Ú", "U")
    nomLieu = nomLieu.replace("Ù", "U")
    nomLieu = nomLieu.replace("Û", "U")
    nomLieu = nomLieu.replace("Ü", "U")
    
    return nomLieu


#on gere les code postal des corse qui ne sont pas au norme 
#les code postaux '22222' et '22223' n'exixte pas (normalement)
def miseAuxNormeCodePostale(codepostale):
    if(codepostale == '2A'):
        return '22222'
    elif(codepostale == '2B'):
        return '22223'
    elif(codepostale[:2]=='2A'):
        return '22222'+ codepostale[2:]
    elif(codepostale[:2]=='2B'):
        return '22223'+ codepostale[2:]


#pour ecrire les requete vu que ct repetitif pour rien
def ecrireRequete(requete):
    fSql.write(str(requete))
    fSql.write('\n')
    fSql.write('/')
    fSql.write('\n')

#creation des dictionnaire/tableau qui sont utiliser pour eviter les doublons de lieu ....
ville = {}
dep = {}
reg = {}
station = []
listTel = []
cptReleve = 1

#on ecrit diredctement le tuple de la France car il a une valeur nul
ecrireRequete("INSERT INTO Lieu VALUES (1000000000, 'FRANCE', null)")




#on boucle pour tout les element du ficher json 1element = un relever meteo
#i contient l'element
for i in data:
    
    
    #on verifie qu'il y a bien un une region, un dept une ville et une station dans i
    
    if ('nom_dept' in i['fields'] and 'nom_reg' in i['fields'] and 'nom' in i['fields'] and 'numer_sta' in i['fields']):
        
        """
        POUR LA TABLE LIEU
        """  
        
        #On regade si la region de i est deja enregister, si non le fait et on ecrit la requte sql (on fait la meme chose pour les dept les ville st les stations)
        if (i['fields']['nom_reg'] not in reg):
            
            
            #on met au norme le nom du lieu pour ne pas qu'il pose de probleme dans oracle
            nomLieu = miseAuxNorme(i['fields']['nom_reg'])
            
            #on cree un id pour chaque region (on met 999 devant puis le code region sur 2 cararter et le tout sur 10 caractere pour avoir une norme)
            idRegion = ('999'+i['fields']['code_reg'].zfill(2)).zfill(10)
            
            #on l'ajoute dans le dicto
            reg[i['fields']['nom_reg']] = idRegion

            
            
            #on ecrit la requet sql
            requete="INSERT INTO Lieu VALUES (" +idRegion+", '"+ nomLieu +"' ,"+ "1000000000)"
            ecrireRequete(requete)
            
            
            
        #voir region   
        if (i['fields']['nom_dept'] not in dep):
            
            nomLieu = miseAuxNorme(i['fields']['nom_dept'])
            
            #on verifie qu on est pas en corse car leurs code postal contient des lettres
            if (i['fields']['code_dep'] == '2A' or i['fields']['code_dep'] == '2B'):
                idDept = (miseAuxNormeCodePostale(i['fields']['code_dep'])).zfill(10)
            else:
                idDept = (i['fields']['code_dep']).zfill(10)
                
                
            dep[i['fields']['nom_dept']] = idDept
            
            #on recalcule l'id pere
            idPere = ('999'+i['fields']['code_reg'].zfill(2)).zfill(10)
            
            requete="INSERT INTO Lieu VALUES (" +idDept+", '"+ nomLieu +"' ,"+idPere +")"
            ecrireRequete(requete)
            
            
        #voir region      
        if (i['fields']['nom'] not in ville):
            
            nomLieu = miseAuxNorme(i['fields']['nom'])
            
            
            if (i['fields']['codegeo'][:2]=='2A' or i['fields']['codegeo'][:2]=='2B'):
                idVille = (miseAuxNormeCodePostale(i['fields']['codegeo'])).zfill(10)
            else:
                idVille = (i['fields']['codegeo']).zfill(10)
            
            ville[i['fields']['nom']] = idVille
            
            if (i['fields']['code_dep'] == '2A' or i['fields']['code_dep'] == '2B'):
                idPere = (miseAuxNormeCodePostale(i['fields']['code_dep'])).zfill(10)
            else:
                idPere = (i['fields']['code_dep']).zfill(10)
            
            requete="INSERT INTO Lieu VALUES (" +idVille+", '"+ nomLieu +"' ,"+idPere +")"
            
            ecrireRequete(requete)
            
        """
        POUR LA TABLE STATION
        """
        
        #voir region     
        if (i['fields']['numer_sta'] not in station):
            station.append(i['fields']['numer_sta'])
            
            
            if (i['fields']['codegeo'][:2]=='2A' or i['fields']['codegeo'][:2]=='2B'):
                idPere = (miseAuxNormeCodePostale(i['fields']['codegeo'])).zfill(10)
            else:
                idPere = (i['fields']['codegeo']).zfill(10)
            
            #on cree un numero de tel sans le 04 
            numTel = 25416378
            while (len(str(numTel))<7 and numTel in listTel):
                numTel = random.randint(0, 99999999)
            listTel.append(numTel)
            
            idStation = i['fields']['numer_sta'].zfill(10)
            
            #on prend les coo gps de la station
            latitude = i['fields']['latitude']
            longitude = i['fields']['longitude']
            
            requete="INSERT INTO Station VALUES (" + idStation + "," + idPere + ", '04" + str(numTel) + "'," + str(latitude) + "," + str(longitude) + ")"
            ecrireRequete(requete)

            
        """
        POUR LA TABLE RELEVE 

        """
        #on cree une liste pour les id releve
        listeReleve = []
        listeReleve.append('0')
        idReleve = '0'
        
        #on met au bon format la date
        jour = i['fields']['date'][8:10]
        mois = i['fields']['date'] [5:7]
        annee = i['fields']['date'] [:4]
        date = jour +"-"+ mois +"-"+ annee
        
        #on cree un id unique
        while(idReleve in listeReleve):  
            idReleve = jour + mois + annee + i['fields']['numer_sta'] + str(cptReleve).zfill(8)
        listeReleve.append(idReleve)
        
        
        requete="INSERT INTO Releve VALUES (" + idReleve +", TO_DATE('"+ date +"' , 'DD-MM-YYYY') ,"+ i['fields']['numer_sta'].zfill(10)+")"
        ecrireRequete(requete)
        
        
        
        
        """
        POUR LES MESURE
        """
        
        #Pour la temperature
        if ('tc' in i['fields']):
            
            idMesure = jour + mois + annee + i['fields']['numer_sta'] + str(cptReleve).zfill(8)+ str(cptReleve) +"01"
        
            requete="INSERT INTO Mesure VALUES ("+idMesure+", 'Temperature', "+ str(round(i['fields']['tc'],2))+" ,"+ idReleve+")"
            ecrireRequete(requete)
            
        
        #la pluie sur les 3 dernier h
        if ('rr3' in i['fields']):
            
            idMesure = jour + mois + annee + i['fields']['numer_sta'] + str(cptReleve).zfill(8)+ str(cptReleve) +"02"
            
        
            requete="INSERT INTO Mesure VALUES ("+idMesure+", 'Pluviometrie',  "+ str(round(i['fields']['rr3'],2))+" ,"+ idReleve+")"
            ecrireRequete(requete)
            
        
        #la force du vent et sa direction
        if ('dd' in i['fields'] and 'ff' in i['fields']):
            
            idMesure = jour + mois + annee + i['fields']['numer_sta'] + str(cptReleve).zfill(8)+ str(cptReleve) +"03"
        
            requete="INSERT INTO Mesure VALUES ("+idMesure+", 'Vent', "+ str(round(i['fields']['ff'] * 3.6, 2)) +" ,"+ idReleve+")"
            ecrireRequete(requete)
            
            
        #l'ensoleillrmrnt ATTENTION c'est une variable aléatoire   
        if (random.randint(0,1)==0):
            idMesure = jour + mois + annee + i['fields']['numer_sta'] + str(cptReleve).zfill(8)+ str(cptReleve) +"04"
            requete="INSERT INTO Mesure VALUES ("+idMesure+", 'Ensoleillement', "+ str(round(random.randint(1400,2500),2)) +" ,"+ idReleve+")"
            
            ecrireRequete(requete)
        
        cptReleve+=1
        
        
"""
POUR LA TABLE ALERTE  ATTENTION valeurs aléatoire   
"""
#list de niveaux d'alerte sans le niv Vert car quand c'est vert ben il n'y a pas d'alerte
niveauxAlerte = ["Rouge", "Orange", "Jaune"]

#liste des type d'alerte
listeAlerte = ['Vent violent', 'Pluie-inondation',  'Inondation', 'Orages' ,'Neige-verglas' ,'Canicule', 'Grand froid', 'Crue']


#on bouble dans le dico des regions
for cle , idReg in reg.items():
    
    #on choisit un nbr alea d'alerte prs region
    nbrAlerte = random.randint(5,18)
    for i in range (nbrAlerte-1):
        
        #on definit la date de debut de l'alerte
        jourDep = random.randint(1,28)
        moisDep = random.randint(1,12)
        dateDep = str(jourDep).zfill(2)+"-"+str(moisDep).zfill(2)+"-"+"2021"
        
        #on definit en fonction de la date de debut la date de fin
        jourFin = jourDep + random.randint(0,10)
        if (jourFin > 28):
            jourFin = jourFin - 28
            moisFin = moisDep + 1
        else:
            moisFin = moisDep
            
        if (moisFin > 12):
            moisFin=1
            dateFin =str(jourFin).zfill(2)+"-"+str(moisFin).zfill(2)+"-"+"2022"
        else:
            dateFin =str(jourFin).zfill(2)+"-"+str(moisFin).zfill(2)+"-"+"2021"
            
        #on choisit dans les liste le niv et la cat 
        cat = random.choice(listeAlerte)
        niveaux = random.choice(niveauxAlerte)
    
        idAlerte = str(jourDep).zfill(2) + str(moisDep) + idReg + str(i)

        requete="INSERT INTO Alerte VALUES ("+idAlerte+", '"+ cat +"' ,"+ idReg +", TO_DATE('"+ dateDep+"' ,'DD-MM-YYYY'), TO_DATE('"+ dateFin +"' ,'DD-MM-YYYY'), '"+ niveaux +"' )"
        ecrireRequete(requete)
        
# on ferme tout les fichier ouvert    
fSql.close()
fVille.close()