<<<<<<< HEAD
import loremipsum as ipsum 
from re import sub,search
DICTIONNAIRE=open("aux").read().split("\n")
RESULTAT={}
#TEXTE=list(map(lambda x:x.split(" "),ipsum.texte().split("\n")))
TEXTE=[["azaz"],["azaz"]]
def recherche(mot,upper=False,propre=False):
    global DICTIONNAIRE,RESULTAT
    mot=sub("[!\.?:,]","",mot)
    if len(mot)==0:
        return True
    if upper:
        mot=mot.lower()
        RESULTAT[mot]=mot in DICTIONNAIRE and "1" or "0"
    else:
        mot=sub("d'|l'|n'|t'|D'|L'|N'|T'|Qu'|qu'","",mot) 
        if mot in DICTIONNAIRE:
            RESULTAT[mot]="1"
        else:
            return recherche(mot,True)
    return RESULTAT[mot]=="1" and True or False
if __name__=="__main__":
    print("\n".join(" ".join(i) for i in TEXTE))
    print("\nCorrection:\n")
    for i in range(len(TEXTE)):
        for j in range(len(TEXTE[i])):
            if not(len(TEXTE[i][j])):
                continue
            if RESULTAT.get(TEXTE[i][j]): 
                if RESULTAT[TEXTE[i][j]]=="0":
                    print(TEXTE[i][j]+"\n\tligne "+str(i+1))
                else:
                    continue
            if j==0 or search("!\.?:",TEXTE[i][j-1][-1]):
                if TEXTE[i][j].islower():
                    print(TEXTE[i][j]+"\n\tligne "+str(i+1)+"\n\tDoit prendre une majuscule")
                else:
                    if(not recherche(TEXTE[i][j])):#nom propre
                        print(TEXTE[i][j]+"\n\tligne "+str(i+1))
            else:
                if(not recherche(TEXTE[i][j])):#nom commun
                    print(TEXTE[i][j]+"\n\tligne "+str(i+1))
=======
#-*- coding:utf-8 -*-
import re
from string import find
import loremipsum as ipsum

def construire_repere():
    lettres=open("lettres","r").read().split()
    repere={}
    for l in lettres:
        repere[l[0:l.find(":")]]=l[l.find(":")+1:len(l)] # donc chaque element du repere est sous une forme lettre[lettre]:numero_de_ligne_du_dico
    return repere

#les deux fonctions sont quasi identiques mais au moment ou j'écris ce commentaire (il est a peu pres 2h du matin) je n'ai pas cherché de solution
def recherche1(mot):#pour les mots de débuts de phrases (Apres un point), la variable mot correspond donc soit a un nom propre, soit a un mot commum, on commence par chercher parmis les noms propres(qui sont moins nombreux), puis ensuite parmis les nom communs du dictionnaire
    global repere,resultat,repere_help,dico# on recupere les variables du main qui nous interressent
    a=repere.get(mot[:2]) #encadrement minimum
    if a == None: # si le debut du mot n'est pas dans le repere alors il n'est pas dans le dico, mais il est peut etre un nom commum alors on relance une recherche en reduisant le mot en lettres minuscules
        return recherche2(mot.lower(),True)
    else:
        a=int(a)
        #encadrement maximum
        try:
            b=int(repere[repere_help[repere_help.index(mot)+1]])
        except:
            b=len(dico)
    if mot in dico[a-1:b]:#si le mot est dans l'encadrement du dico
        resultat[mot]="1"
        return
    else:
        return recherche2(mot.lower(),True)#sinon peut etre nom commum
def recherche2(mot,upper=False): #pour les noms communs et les noms propres
    global repere,resultat,repere_help,dico
    a=repere.get(mot[0:2])
    if a == None:
        if upper:
            mot=mot[0].upper()+mot[1:]
        resultat[mot]="0"
        return 
    else:
        a=int(a)
        try:
            b=int(repere[repere_help[repere_help.index(mot)+1]])
        except:
            b=len(dico)
    if mot in dico[a-1:b]:
        if upper:
            mot=mot[0].upper()+mot[1:]
        resultat[mot]="1"
        return
    else:
        if upper:
            mot=mot[0].upper()+mot[1:]
        resultat[mot]="0"
#MAIN---------------------------------------------------
resultat={} #on stocke les resultats des recherches afin de ne pas faire des calculs deja effectués
dico=open("aux","r").read().split() 
repere=construire_repere() #on recupere le repere de lettre sous la forme d'un dictionnaire
repere_help=sorted(repere) #cette liste permet de savoir quel est le prochain element du repere pour faciliter l'encadrement par exemple si on prendre le mot "thomas", il est situé entre th et ti dans le repere
texte=ipsum.texte().split("\n") # on prend un texte aléatoire et on le découpe ligne par ligne
for i in range(len(texte)):
    texte[i]=texte[i].split(" ") #pour chaque ligne du texte, on la découpe entre les espaces
    for k in range(len(texte[i])):
        if len(texte[i][k])==0: # si le mot est vide pas de recherche
            continue
        elif texte[i][k] in resultat: #si le mot est dans la liste des resultats
            if resultat[texte[i][k]]=="0":
                print texte[i][k],i+1
            continue
        #netoyage
        mot=re.sub("d'|l'|n'|qu'|t'|[:.,;!?%]","",texte[i][k]) #nettoyage
        #premier mot d'une phrase
        if ((k == 0 ) or (len(texte[i][k-1])>0 and ((texte[i][k-1][-1]==".") or (texte[i][k-1][-1]=="!") or (texte[i][k-1][-1]=="?" )))): 
            recherche1(mot)
        #nom propre ou nom commun
        else:
            recherche2(mot)
        if resultat[mot]=="0":
            print texte[i][k],i
>>>>>>> 774ded8962c19d7226574d7fba4e3949acd54220
