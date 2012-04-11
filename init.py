#-*- coding:utf-8 -*-
def cmpval(x,y):#pour trier le dictionnaire
    if x[1]<y[1]:
        return -1
    elif x[1]==y[1]:
        return 0
    else:
        return 1
lines=sorted(open("mots","r").read().split())
open("aux","w").write("".join(i+"\n" for i in lines))
collecteur={}
ligne=1
for i in lines:
    if len(i)>1:
        if collecteur.get(i[0:2])==None:
            collecteur[i[0:2]]=ligne
    if len(i)==1:
        if collecteur.get(i[0])==None:
            collecteur[i[0]]=ligne
    ligne+=1
collecteur=collecteur.items()
collecteur.sort(cmpval)
open("lettres","w").write("".join(n[0]+":"+str(n[1])+"\n" for n in collecteur))
