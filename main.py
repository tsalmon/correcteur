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
