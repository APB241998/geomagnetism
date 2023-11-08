#import des librairies utilisees
import re
import matplotlib.pyplot as plt
import sys


#########################################################################################################################################


#definition des fichiers de mesure
#definition du dossier si pas au meme endroit que le script
sys.path.append('M:\\Appl\\DATA\\PROD\\vermessung\\Geodaetische_Grundlagen\\7-Geomagnetik')
#definition des noms de fichiers a utiliser
file_names =['wichtrach_1_20231005.csv','wichtrach_2_20231005.csv','wichtrach_1_20231011.csv','wichtrach_2_20231011.csv']


#definition du nombre de serie pour les plots 
no_series = []
for i in range(0,len(file_names)) :
    no_series.append(i+1)


#########################################################################################################################################


#fonction d'import des valeurs mesures par le theodolite H, V, valeur du senseur, scalaire geo, heure UTC
def importMesuresValues(file_name):
    #creation d'un dictionnaire pour stocker les valeurs
    dict_Mesures = {}
    #ouverture du fichier entre en parametres
    file = open(file_name, 'r')
    #lecture des lignes du fichier
    lines = file.readlines()
    
    #recherche et creation d'une variable date 
    data = lines[1].split('\t')
    date = data[1]
    
    #boucle sur les lignes du fichier contenant les valeurs mesurees
    for line in lines[32:45]:
        #indication du separateur de lignes 
        data = line.split('\t')
        #creation d'une variable avec le numero de point (ajoute automatiquement lors des mesures)
        no = data[0]
        #creation d'une variable du type de configuration de la position mesuree
        sensor_pos = data[1]
        #creation d'une variable pour l'angle horizontal donne en dms
        H = str(data[2])
        #separation des degres, minutes, secondes
        x = re.split("\s",H)
        #valeur deg
        a = int(x[0][:-2])
        #valeur minute
        b = int(x[1][:-1])
        #valeur seconde
        c = float(x[2][:-1])
        #calcul deg en degres decimals et arrondir a  4 decimales
        H_deg = round((a + b/60 + c/3600),4)
        #creation de la valeur en degres minutes secondes
        H_dms = str(a) + str("°") + str(b) + str("'") + str(c) + str("''")
        #creation d'une variable pour l'angle vertical donne en dms
        V = str(data[3])
        #sparation des degrs, minutes, secondes
        y = re.split("\s",V)
        #valeur deg
        d = int(y[0][:-2])
        #valeur minute
        e = int(y[1][:-1])
        #valeur seconde
        f = float(y[2][:-1])
        #calcul deg en degres decimals et arrondir a  4 decimales
        V_deg = round((d + e/60 + f/3600),4)
        #creation de la valeur en degres minutes secondes
        V_dms = str(d) + str("°") + str(e) + str("'") + str(f) + str("''")
        #creation de la variable de la valeur du senseur
        sensor_value = float(data[4])
        #creation de la variable scalaire geo
        scalar_magn = float(data[5])
        #creation de la valeur de l'heure UTC
        time_UTC = data[6].strip()
        
        #import dans le dictionnaire de sortie les valeurs voulues
        dict_Mesures.update({(no,sensor_pos):[{'H_dms':H_dms},{'H_deg':H_deg},{'V_dms':V_dms},{'V_deg':V_deg},{'sensor_value':sensor_value},{'scalar_magn':scalar_magn},{'time_UTC':time_UTC},{'day':date}]})
    #fermeture du fichier donne en parametres
    file.close()  
    
    #retour un dictionnaire avec les valeurs ajoutees
    return dict_Mesures
  

#########################################################################################################################################


#fonction d'import de Absolute Magnetic Observations
def importAbsoluteMagneticObs(file_name):
    #creation d'un dictionnaire pour stocker les valeurs
    dict_Mesures = {}
    #ouverture du fichier entre en parametres
    file = open(file_name, 'r')
    #lecture des lignes du fichier
    lines = file.readlines()

    #recherche et creation d'une variable date 
    data = lines[1].split('\t')
    date = data[1]

    #boucle sur les lignes du fichier contenant les observations magnetiques absolues
    for line in lines[48:50]:
        #indication du separateur de lignes 
        data = line.split('\t')
        #creation d'une variable sur l'info declination ou inclination
        typ = data[0]
        #creation d'une variable pour l'angle donne en dms
        dms = data[1]
        #separation des degres, minutes, secondes
        x = re.split("\s",dms)
        #valeur deg
        a = int(x[0][:-2])
        #valeur minute
        b = int(x[1][:-1])
        #valeur seconde
        c = float(x[2][:-1])
        #creation de la valeur en degres minutes secondes
        dms = str(a) + str("°") + str(b) + str("'") + str(c) + str("''")
        #creation de la valeur en degres decimaux
        deg = float(data[2])
        #creation de la valeur en gon
        gon = float(data[3])
        
        #import dans le dictionnaire de sortie les valeurs voulues
        dict_Mesures.update({(typ):[{'dms':dms},{'deg':deg},{'gon':gon},{'day':date}]})
    #fermeture du fichier donne en parametres
    file.close()  

    #retour un dictionnaire avec les valeurs ajoutees
    return dict_Mesures


#########################################################################################################################################


#fonction d'import des parametres DIM
def importDIMParameters(file_name):
    #creation d'un dictionnaire pour stocker les valeurs
    dict_Mesures = {}
    #ouverture du fichier entre en parametres
    file = open(file_name, 'r')
    #lecture des lignes du fichier
    lines = file.readlines()

    #recherche et creation d'une variable date 
    data = lines[1].split('\t')
    date = data[1]
    
    #boucle sur les lignes du fichier contenant les parametres DIM
    for line in lines[53:56]:
        #indication du separateur de lignes 
        data = line.split('\t')
        #creation d'une variable du nom du parametres (horizontal collimation error, vertical collimation error from D and I series)
        param = data[0]
        #creation de la valeur en degres decimaux
        deg = float(data[2])
        #creation d'une variable pour l'angle donne en dms
        dms = data[1]
        #separation des degres, minutes, secondes
        x = re.split("\s",dms)
        #valeur deg
        a = int(x[0][:-2])
        #valeur minute
        b = int(x[1][:-1])
        #valeur seconde
        c = float(x[2][:-1])
        #creation de la valeur en degres minutes secondes
        #avec condition que si la valeur en degres decimaux est negative, il ajoute un "-" car il n'est pas conserve en separant les dms
        if deg <0:  
            dms = str('-') + str(a) + str("°") + str(b) + str("'") + str(c) + str("''")
        #si pas negative, ne pas ajouter de "-"
        else:
            dms = str(a) + str("°") + str(b) + str("'") + str(c) + str("''")     
        #creation de la valeur en mgon
        mgon = float(data[3])
        
        #import dans le dictionnaire de sortie les valeurs voulues
        dict_Mesures.update({(param):[{'dms':dms},{'deg':deg},{'mgon':mgon},{'day':date}]})
    #fermeture du fichier donne en parametres
    file.close()  

    #retour un dictionnaire avec les valeurs ajoutees
    return dict_Mesures


#########################################################################################################################################


#fonction d'import des offset
def importOffset(file_name):
    #creation d'un dictionnaire pour stocker les valeurs
    dict_Mesures = {}
    #ouverture du fichier entre en parametres
    file = open(file_name, 'r')
    #lecture des lignes du fichier
    lines = file.readlines()
    
    #recherche et creation d'une variable date 
    data = lines[1].split('\t')
    date = data[1]

    #boucle sur les lignes du fichier contenant les offset nT
    for line in lines[56:58]:
        #indication du separateur de lignes 
        data = line.split('\t')
        #creation de la variable du type d'offset
        offset = data[0]
        #creation de la variable de la valeur du offset
        nT = float(data[1][:-4])
        
        #import dans le dictionnaire de sortie les valeurs voulues
        dict_Mesures.update({(offset):[{'nT':nT},{'day':date}]})
    #fermeture du fichier donne en parametres
    file.close()
    
    #retour un dictionnaire avec les valeurs ajoutees
    return dict_Mesures


#########################################################################################################################################


#fonction d'import de tous les parametres mesures
def importTOT(file_name):
    
    mes_val = importMesuresValues(file_name)
    decl_incl = importAbsoluteMagneticObs(file_name)
    DIM_param = importDIMParameters(file_name)
    offset = importOffset(file_name)
    
    return mes_val, decl_incl, DIM_param, offset


#########################################################################################################################################


#creation de listes avec les valeurs des series pour les utiliser dans les plots
#list des valeurs de declinaison
list_decl = []
#liste des valeurs d'inclinaison
list_incl = []
#liste des valeurs de collimation horizontale
list_coll_h = []
#liste des valeurs de collimation verticale serie D
list_coll_v_D = []
#liste des valeurs de collimation verticale serie I
list_coll_v_I = []
#liste des valeurs de offset D
list_offset_D = []
#liste des valeurs de offset I
list_offset_I = []

#utilisation des fonctions
#les mesures et les listes s'importent automatiquement peu importe le nombre de fichiers de serie
for i in range(0,len(file_names)):  
    globals()['mes_val_'+str(i+1)] = importMesuresValues(file_names[i])
    globals()['decl_incl_'+str(i+1)] = importAbsoluteMagneticObs(file_names[i])
    globals()['DIM_param_'+str(i+1)] = importDIMParameters(file_names[i])
    globals()['offset_'+str(i+1)] = importOffset(file_names[i])  
    list_decl.append(globals()['decl_incl_'+str(i+1)]['Declination, D:'][1]['deg'])
    list_incl.append(globals()['decl_incl_'+str(i+1)]['Inclination, I:'][1]['deg'])
    list_coll_h.append(globals()['DIM_param_'+str(i+1)]['Horizontal collimation error, delta angle:'][1]['deg'])
    list_coll_v_D.append(globals()['DIM_param_'+str(i+1)]['Vertical collimation error, epsilon angle (from D series):'][1]['deg'])
    list_coll_v_I.append(globals()['DIM_param_'+str(i+1)]['Vertical collimation error, epsilon angle (from I series):'][1]['deg'])
    list_offset_D.append(globals()['offset_'+str(i+1)]['Offset (from D series):'][0]['nT'])
    list_offset_I.append(globals()['offset_'+str(i+1)]['Offset (from I series):'][0]['nT'])

    
#########################################################################################################################################


#plot des series
#ferme les plots ouverts pour le relancement des calculs
plt.close('all')

#plot du graphique des resultats de l'observation magnetique absolue
fig1, (ax1,ax2) = plt.subplots(2)
fig1.suptitle('Resultats observation magnetique absolue')
#declinaison
ax1.plot(no_series,list_decl,'r--o')
ax1.set_xlabel('No serie')
ax1.set_ylabel('Declinaison [deg]')
plt.sca(ax1)
plt.xticks(no_series)
plt.yticks(list_decl)
#inclinaison
ax2.plot(no_series,list_incl,'b--o')
ax2.set_xlabel('No serie')
ax2.set_ylabel('Inclinaison [deg]')
plt.sca(ax2)
plt.xticks(no_series)
plt.yticks(list_incl)

#plot du graphique des erreurs de collimation
fig2, (ax1,ax2,ax3) = plt.subplots(3)
fig2.suptitle('Erreurs de collimation')
#collimation horizontale
ax1.plot(no_series,list_coll_h,'c--o')
ax1.set_xlabel('No serie')
ax1.set_ylabel('Horizontal [deg]')
plt.sca(ax1)
plt.xticks(no_series)
plt.yticks(list_coll_h)
#collimation verticale serie D
ax2.plot(no_series,list_coll_v_D,'y--o')
ax2.set_xlabel('No serie')
ax2.set_ylabel('Vertical D [deg]')
plt.sca(ax2)
plt.xticks(no_series)
plt.yticks(list_coll_v_D)
#collimation verticale serie I
ax3.plot(no_series,list_coll_v_I,'k--o')
ax3.set_xlabel('No serie')
ax3.set_ylabel('Vertical I [deg]')
plt.sca(ax3)
plt.xticks(no_series)
plt.yticks(list_coll_v_I)

#plot du graphique des offset
fig3, (ax1,ax2) = plt.subplots(2)
fig3.suptitle('Offset')
#offset serie D
ax1.plot(no_series,list_offset_D,'m--o')
ax1.set_xlabel('No serie')
ax1.set_ylabel('Offset D [nT]')
plt.sca(ax1)
plt.xticks(no_series)
plt.yticks(list_offset_D)
#offset serie I
ax2.plot(no_series,list_offset_I,'g--o')
ax2.set_xlabel('No serie')
ax2.set_ylabel('Offset I [nT]')
plt.sca(ax2)
plt.xticks(no_series)
plt.yticks(list_offset_I)

plt.show()


#########################################################################################################################################