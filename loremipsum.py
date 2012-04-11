#-*- coding:utf-8 -*-
from random import choice
def texte():
    l1=["J'ai mangé","J'ai truqué","J'ai battu","J'ai aimé","Un gars a écrasé","Un type a avalé","Un jour j'ai renversé","j'ai dessiné"]
    l2=["un petit gros","une barbie","le président","l'Univers","le Pentagone","une banane","une pomme","un éléphant","ma voiture","un truc","l'anneau","kirikou","Dieu si il existe","le mec là"]
    l3=["sans faire exprès.","comme ça.","et ça a fait des chocapix.","parce que je le vaut bien.","et alors?","quand j'avais huit ans.","en Ouzbékistan.","parce que je suis ton père.","et puis voila quoi !","mais j'ai oublié la suite.","et toi?","m'a-t-on dit.","mais je l'aime quand même","mais il est fou?","car c'était nécessaire.","car j'avais trop faim.","car j'avais trop soif.","bonne idée, hein?"]
    return "".join(choice(l1)+" "+choice(l2)+", "+choice(l3)+choice([" "," Ah et puis: ","\n"]) for i in range(2))+"".join(choice(l1)+" "+choice(l2)+", "+choice(l3)+choice([" ","\n"]) for i in range(2)) 

