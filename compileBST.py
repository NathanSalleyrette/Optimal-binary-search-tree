#!/usr/bin/env python3
import sys
import time
import math


def read_file(nom_fichier, n):
  """
  lit le fichier et remplit 2 listes SumFreq et Freq
  """
  try:
    fichier = open(nom_fichier, "r")
  except FileNotFoundError:
    raise Exception("File Not Found")
  Sum_Freq = [0 for _ in range(n)]
  Freq = [0 for _ in range(n)]
  id = 0
  precedent = 0
  for ligne in fichier:
    for mot in ligne.split():
      Sum_Freq[id] = int(mot) + precedent
      Freq[id] = int(mot)
      precedent = Sum_Freq[id]
      id += 1
  return Freq, Sum_Freq


"""
Freq = [5, 4, 8, 8, 10]
Sum_Freq = [5, 9, 17, 25, 35]
"""

def sum(i, j, Sum_Freq):
    if i == 0:
        return Sum_Freq[j]
    else:
        return Sum_Freq[j] - Sum_Freq[i-1]


def cout(nom_fichier, n):
    """
    renvoie les matrices contenant les couts successifs et les racines obtenues
    en appliquant l'algorithme de Bellman
    """
    Freq, Sum_Freq = read_file(nom_fichier, n)
    racines = [[0 for _ in range(n-i+1)]for i in range(n)]
    couts = [[0 for _ in range(n-i+1)]for i in range(n+1)]
    for i in range(n):
        couts[i][0] = 0
        couts[i][1] = Freq[i]
        racines[i][0] = i
    for j in range(n):
        for i in range(j, -1, -1):
            somme_ij = sum(i,j,Sum_Freq)
            min = math.inf
            rac = i
            for k in range(i, j+1):
                C = couts[i][k-i] + couts[k+1][j-k] + somme_ij
                if C < min:
                    min, rac = C, k
            couts[i][j-i+1]=min
            racines[i][j-i+1] = rac
    return couts, racines


def reconstruction_arbre(racines, n):
    t = [[-1, -1] for k in range(n)]
    point_de_depart = racines[0][n]
    # On doit trouver le/les fils de l'arbre optimal dans les indices compris entre ind(inclus) et supp -i avec ind comme racine
    def reconstruction_recursive(ind, supp, inf):
        # Cas de base
        if (inf + 1 == supp):
            return
        # Cas où on est trop a gauche donc on a que des fils droits
        if ind == inf:
            fils_droit = racines[ind+1][supp-ind-1]
            t[ind] = [-1, fils_droit]
            reconstruction_recursive(fils_droit, supp, ind + 1)
        #Cas où on est trop a droite donc on a que des fils gauches
        elif ind == (supp - 1):
            fils_gauche = racines[inf][(ind - inf)]
            t[ind] = [fils_gauche, -1]
            reconstruction_recursive(fils_gauche, ind, inf)
        #Cas général
        else:
            fils_gauche = racines[inf][ind - inf]
            fils_droit = racines[ind+1][supp-ind-1]
            t[ind] = [fils_gauche, fils_droit]
            #print(tableau_final)
            reconstruction_recursive(fils_gauche, ind, inf)
            reconstruction_recursive(fils_droit, supp, ind+1)
    reconstruction_recursive(point_de_depart, n, 0)
    return point_de_depart, t


def joli_affichage(couts, racines, t, n):
  # Depth n'était pas demandé mais on peut le renvoyer avec l'instruction ci-dessous
  # print("static long BSTdepth = " + str(couts[0][n]) +";")
  print("static int BSTroot = " + str(racines[0][n]) + ";")
  print("static int BSTtree[" + str(n) + "][2] = {")
  for i in range(n):
    print("{" + str(t[i][0]) + "," + str(t[i][1]) + "}, ")
  print(" };")


def main():
  arguments = sys.argv
  if len(arguments) != 3:
    print("Erreur !!! La commande doit être de la forme: ./abr.py n fichier_texte !!!\n")
    return
  nom_fichier = arguments[2]
  n = int(arguments[1])
  temps1 = time.time()
  couts, racines = cout(nom_fichier, n)
  point_de_depart, t = reconstruction_arbre(racines, n)
  joli_affichage(couts, racines, t, n)
  temps2 = time.time()
  print("temps de calcul = " + str(temps2 - temps1))


main()
