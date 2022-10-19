import numpy as np
import matplotlib.pyplot as plt
import random as rd

def tas_conique(diametre , hauteur):

    taille_matrice = diametre*3//2
    rayon=diametre//2
    pente = hauteur/rayon
    milieu = taille_matrice//2

    mat = np.zeros((taille_matrice,taille_matrice))

    for ind_ligne in range(rayon): #les n premieres lignes avec n = diametre
        for ind_col in range(rayon):
            distance = np.sqrt(ind_ligne**2+ind_col**2) #distance par rapport au milieu

            if distance <= rayon:
                empilement = int(hauteur - distance*pente)
                mat[milieu - ind_ligne][milieu - ind_col] = empilement
                mat[milieu + ind_ligne][milieu - ind_col] = empilement
                mat[milieu - ind_ligne][milieu + ind_col] = empilement
                mat[milieu + ind_ligne][milieu + ind_col] = empilement
    return mat

#REGLES
#La regle unidirectionnelle concerne le déplacement des grains du au courant avant le sommet
#La regle effondrement concernent davatange l'effondrement qui intervient après le sommet, elle est complémentaire des regles 'courant'

def regle_unidirectionnelle(mat):
    new_mat = mat.copy()
    for ligne in range(1,len(mat)-1):
        for colonne in range(len(mat)-1):

            if (mat[ligne-1][colonne] < mat[ligne][colonne]) and (mat[ligne+1][colonne] <= mat[ligne][colonne] + 1) :
                #Contraintes sur les hauteurs de tas de devant et derrière
                new_mat[ligne][colonne] = new_mat[ligne][colonne] - 1
                new_mat[ligne+1][colonne] += 1
    return new_mat

def nombre_de_grains_qui_tombent(delta_hauteur):
    nb_effondres = int((delta_hauteur+2.0)/2 * rd.random()) + 1 #D'apres le sujet O en info à Mines - Pont
    return nb_effondres

def regle_effondrement(mat):
    mat_new = mat.copy()
    for i in range(len(mat)-1):
        for j in range(len(mat)):
            delta_hauteur = mat[i][j]-mat[i+1][j]

            if delta_hauteur > 1:
                grains_qui_tombent = nombre_de_grains_qui_tombent(delta_hauteur)
                mat_new[i][j] -= grains_qui_tombent
                mat_new[i+1][j] += grains_qui_tombent

    return mat_new

#Programme pour appliquer les règles

def application_regle(mat, ite):
    mat_finale = mat.copy()

    for k in range(ite):
        mat_finale = regle_effondrement(regle_unidirectionnelle(mat_finale))

    return mat_finale


#Anayse et determination de caracteristiques

def hauteur_barcane(mat):
    return max([max(liste) for liste in mat])

def coord_hauteur(mat):
    ind_ligne = 0
    maxi = hauteur_barcane(mat)

    for i in range(len(mat)):
        if max(mat[i]) == maxi:
            ind_ligne = i
    return ind_ligne

def longueur(mat):
    taille_matrice = len(mat)
    ind1,ind2 = 0,taille_matrice - 1
    for ind_ligne in range(taille_matrice-1):

        ligne1,ligne2 = mat[ind_ligne],mat[ind_ligne+1]

        if max(ligne1)==0 and max(ligne2)> 0 :
            ind1 = ind_ligne +1

        if max(ligne1)>0 and max(ligne2) ==0 and (ind1 != 0) :
            ind2 = ind_ligne
    longueur = ind2 - ind1 + 1
    return longueur

def largeur(mat):
    mat_transpo = mat.transpose()
    largeur = longueur(mat_transpo)
    return largeur

def largeur2(mat):
    cote_gauche, cote_droit = 0,0
    i_hauteur = coord_hauteur(mat) #numero de ligne de la hauteur

    for j in range(len(mat)-1):
        if mat[i_hauteur][j] ==0 and mat[i_hauteur][j+1] !=0:
            cote_gauche = j
        elif mat[i_hauteur][j] !=0 and mat[i_hauteur][j+1] ==0:
            cote_droit = j
    return cote_droit - cote_gauche +1

#Présentation

def affichage_2D(mat):

    abscisse =[]
    ordonnee = []
    empilements = []
    taille_matrice = len(mat)
    for i in range(taille_matrice):
        for j in range(taille_matrice):
            abscisse.append(i)
            ordonnee.append(j)
            empilements.append(mat[i][j])


    plt.scatter(abscisse, ordonnee,c=np.array(empilements),s=100,marker = 's')
    plt.show()

#Expérience

def experience_unique(diametre, hauteur, ite):

    #Execution
    A = tas_conique(diametre , hauteur)
    taille_matrice = (diametre*3)//2
    rayon = diametre//2
    masse = 2500*np.pi*(hauteur/3)*(rayon)**2 #à partir du volume d'un cone

    affichage_2D(A)
    print("Etat initial")
    print("Taille matrice : ", taille_matrice)
    print("Diametre : ", diametre)
    print("Hauteur : ", hauteur)
    print("Masse : ", masse)
    coordhauteur1 = coord_hauteur(A)

    B = application_regle(A,ite)
    affichage_2D(B)
    print("Etat final")
    print("Itérations : ", ite)
    print("Hauteur : ",hauteur_barcane(B))
    print("Longueur : ", longueur(B))
    print("Largeur : ", largeur2(B))
    coordhauteur2 =  coord_hauteur(B)
    distance = coordhauteur2 - coordhauteur1
    print("Distance parcourue : ", distance)


def experience_serie_distance(diametre,hauteur):

    A = tas_conique(diametre , hauteur)
    taille_matrice = 75 # arbitraire, choisie de telle sorte que les dunes ne sortent pas du cadre de la matrice au bout d'un certain temps et faussent les valeurs
    rayon = diametre//2
    masse = 2500**np.pi*(hauteur/3)*(rayon)**2
    coordhauteur1 = coord_hauteur(application_regle(A, 100)) #formation de la dune initiale

    distances = []

    for i in range(1, 18): #arbitraire, 18 valeurs obtenues
        ite = 50*i #arbitraire, on ajoute 50 pour chaque dune
        B = application_regle(A,ite)
        coordhauteur2 = coord_hauteur(B)
        distance = coordhauteur2 - coordhauteur1 #mesure distance par la difference de coordonnée des points de la hauteur
        distances.append(distance)

    return distances

def experience_serie(depart_diametre,fin_diametre,pas):

    #Parametrage interne
    taille_matrice = 2*fin_diametre
    ratio_hd = 1/3 # peut être modifié mais un rapport d'aspect trop faible (plus proche de la réalité, 1/10 par ex.) ne permet pas de former des dunes correctes

    #Execution
    longueurs, largeurs, hauteurs = [],[],[]
    numero_du_tas = 0

    for diametre in range(depart_diametre,fin_diametre,pas):
        numero_du_tas += 1

        intervalle = (fin_diametre - depart_diametre)/pas

        A = tas_conique(diametre , int(diametre*ratio_hd))
        A = application_regle(A, int(diametre*5)) # nombre d'itérations arbitraire, ici choisi adapté pour que la dune ne sorte pas de l'affichage (on peut modifier taille_matrice sinon aussi) et pour qu'elle garde une forme cohérente (les dunes ne sont pas stables, elles se désagrègent si trop d'itérations)
        affichage_2D(A)
        print(numero_du_tas,"/", intervalle)
        longueurs.append(longueur(A))
        largeurs.append(largeur(A))
        hauteurs.append(hauteur_barcane(A))

    plt.plot(longueurs,largeurs)
    plt.xlabel("Longueur")
    plt.ylabel("Largeur")
    plt.show()

    plt.plot(longueurs,hauteurs)
    plt.xlabel("Longueur")
    plt.ylabel("Hauteur")
    plt.show()

    return hauteurs, longueurs, largeurs

