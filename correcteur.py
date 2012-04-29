import sys,os.path
from re import sub,search
from tkinter import *


sys.argv.append("-f")
sys.argv.append("test.txt")
sys.argv.append("-g")
#*-*-*-*-*--*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-*-*
#est ce que la ligne de commande correspond a correcteur -f monfichier [-i [monfichier2]]
if(len(sys.argv)<3 or len(sys.argv)>5 or sys.argv[1]!="-f" or (len(sys.argv)==4 and not(sys.argv[3]=="-s" or sys.argv[3]=="-i" or sys.argv[3]=="-g")) or (len(sys.argv)==5 and sys.argv[3]!="-i")):
    print("Erreur de syntaxe dans la ligne de commande")
    exit()
#verifier que le fichier a lire existe
if(not os.path.isfile(sys.argv[2])):
    print("Le fichier "+"'"+sys.argv[2]+"'"+" n'existe pas")
    exit()
if(not os.path.isfile("user")):
    open("user","w").write("");
    
#----------------------------------------------------------

DICTIONNAIRE=list(set(open("mots").read().split("\n"))|(set(open("user").read().split("\n"))))
RESULTAT={}
TEXTE=list(map(lambda x:x.split(" "),open(sys.argv[2]).read().split("\n")))

#1 : premier mot, 2 : propre , 3 : commun
def affectation(mot,aux,val):
    global RESULTAT
    RESULTAT[mot]=val
    if aux != mot:
        RESULTAT[aux]=val
    
    return val=="1"

def partie1(mot,option):
    global DICTIONNAIRE,RESULTAT
    aux=sub("d'|l'|n'|t'|D'|L'|N'|T'|Qu'|qu'|[!:\.\?,]","",mot) 
    if search("^[0-9]+[\.\,]?[0-9]*$",mot) or aux in DICTIONNAIRE:
        return affectation(mot,aux,"1")
    elif option==1 or option==2:
        aux=aux.lower()
        if aux in DICTIONNAIRE:
            return affectation(mot,aux,"1")
        else:
            return affectation(mot,aux,"0")
    else:
        return affectation(mot,aux,"0")
    
def sugg(mot):
    liste=[]
    
    liste.append(mot.replace("a","e",1))
    liste.append(mot.replace("e","a",1))
    liste.append(mot.replace("u","o",1))
    liste.append(mot.replace("o","u",1))
    liste.append(mot.replace("a","ha",1))
    liste.append(mot.replace("e","he",1))
    liste.append(mot.replace("i","hi",1))
    liste.append(mot.replace("o","ho",1))
    liste.append(mot.replace("u","hu",1))
    liste.append(mot.replace("mn","nm",1))
    liste.append(mot.replace("nm","mn",1))
    liste.append(mot.replace("k","c",1))
    liste.append(mot.replace("k","qu",1))
    liste.append(mot.replace("en","an",1))
    liste.append(mot.replace("an","en",1))
    liste.append(mot.replace("o","au",1))
    liste.append(mot.replace("au","o",1))
    liste.append(mot.replace("au","eau",1))
    liste.append(mot.replace("eau","eaux",1))
    liste.append(mot.replace("f","ph",1))
    liste.append(mot.replace("ph","f",1))
    liste.append(mot.replace("g","j",1))
    liste.append(mot.replace("j","g",1))
    liste.append(mot.replace("ss","c",1))
    liste.append(mot.replace("c","ss",1))
    liste.append(mot.replace("-","'",1))
    liste.append(mot.replace("er","é",1))
    liste.append(mot.replace("e","é",1))
    liste.append(mot.replace("er","et",1))
    if mot[-2:]=="an" or mot[-2:]=="en":
        liste.append(mot+"d")
        liste.append(mot+"t")
    if mot[-1]=="r":
        liste.append(mot+"e")
    if mot[-2:]=="ai":
        liste.append(mot+"s")
    if mot[-1]=="o":
        liste.append(mot+"t")
        liste.append(mot+"p")
    liste.append(mot[0].upper()+mot[1:])
    liste=list(set(liste))
    if mot in liste:
        liste.remove(mot)
    return liste

SUGG={}
TESTS=[]
def partie2(mot,base,lvl=0):
    for i in sugg(mot):
        #si le mot a deja été testé on passe au suivant
        if not i in TESTS:
            continue
        TESTS.append(i)
        if (SUGG.get(base)==None or not(i in SUGG[base]))  and (i in DICTIONNAIRE) :
            if SUGG.get(base)==None:
                SUGG[base]=i
            else:
                SUGG[base]+=" "+i
        elif lvl!=2 and (SUGG.get(base)==None or len(SUGG[base].split(" "))<5):
            partie2(i,base,lvl+1)
def afficher_suggestions(texte):
    global SUGG,TESTS
    partie2(texte,texte)
    print(SUGG.get(texte) and "\t"+SUGG[texte] or "\tPas de suggestions")
    TESTS={}
"""
Pour chaque ligne du texte:
   Pour chaque mot de la ligne:

      Est ce que le mot est vide ou est une ponctuation:
          suivant

      Est ce que le mot a deja ete traite:
          Est ce que le mot est faux:
              Afficher le mot et la ligne
              Est ce que la suggestion est demandé :
                  afficher resultat de la recherche dans le dictionnaire des suggestions du mot
          suivant

      Est ce que le mot est le premier de la ligne ou le debut d'une phrase(Soit un nom propre, soit un nom commun):
          Est ce que la premiere lettre n'est une majuscule:
               Afficher le mot et la ligne
               Est ce que la suggestion est demandé:
                   Est ce que (recherche mot dans le dictionnaire sans option) est Vrai:
                     Suggerer le mot avec une majuscule
                   Sinon:
                     afficher resultat recherche dans le dico des suggestions du mot avec une majuscule pour chaque suggestions
 
      OU Est ce que le mot est ecrit en majuscule(c'est donc un nom propre):
           Est ce que(lancer une recherche de validation avec comme option propre) est Faux:
               Afficher le mot et la ligne
               Est ce que la suggestion est demandé:
                    afficher resultat recherche dans le dico des suggestions du mot

      Sinon (le mot est ecrit en minuscule, c'est donc un nom commun):
           Est ce que (lancer une recherche sans options) est Faux:
              Afficher le mot et la ligne
              Est ce que la suggestion est demandé:
                  afficher resultat recherche dans le dico des suggestions du mot
"""
CHOIX={}
def choix(mot):
     global CHOIX
     CHOIX[mot]=input("Faites votre choix\n\t")
def correction(suggestion=False,correction=False):
    global SUGG,RESULTAT,DICTIONNAIRE
    for i in range(len(TEXTE)):
        for j in range(len(TEXTE[i])):
            if not(len(TEXTE[i][j])) or search("[!,\.\?:]",TEXTE[i][j][0]):
                continue
            elif RESULTAT.get(TEXTE[i][j]):
                if(RESULTAT[TEXTE[i][j]]=="0"):
                    print(TEXTE[i][j]+"\n\tligne "+str(i+1))
                    if suggestion:
                        print(SUGG.get(TEXTE[i][j]) and "\n\t"+SUGG[TEXTE[i][j]] or "Pas de suggestions")
                        if correction:
                            choix(TEXTE[i][j])
                continue
            
            if j==0 or search("[!\.\?:]",TEXTE[i][j-1]): #premier mot de la ligne ou d'une phrase
                if not TEXTE[i][j][0].isupper():
                    print(TEXTE[i][j]+"\n\tligne "+str(i+1))
                    if partie1(TEXTE[i][j],1):
                        print("\t"+TEXTE[i][j][0].upper()+TEXTE[i][j][1:])
                    if suggestion:
                          afficher_suggestions(TEXTE[i][j])
                    if correction:
                          choix(TEXTE[i][j])
                    
                elif not partie1(TEXTE[i][j],1):
                    print(TEXTE[i][j]+"\n\tligne "+str(i+1))
                    if suggestion:
                        afficher_suggestions(TEXTE[i][j])
                        if correction:
                            choix(TEXTE[i][j])
            elif not TEXTE[i][j].islower():
                if not partie1(TEXTE[i][j],2):
                    print(TEXTE[i][j]+"\n\tligne "+str(i+1))
                    if suggestion:
                        afficher_suggestions(TEXTE[i][j])
                        if correction:
                            choix(TEXTE[i][j])
            else:
                if not partie1(TEXTE[i][j],3):
                    print(TEXTE[i][j]+"\n\tligne "+str(i+1))
                    if suggestion:
                        afficher_suggestions(TEXTE[i][j])
                        if correction:
                            choix(TEXTE[i][j])

#on utilise cette classe pour afficher des messages d'erreurs
class pop_up:
    def __init__(self,message,dim_x=200,dim_y=100):
        self.root=Tk()
        #pour ne pas pouvoir redimensionner la fenetre
        self.root.resizable(width=False, height=False)
        self.root.title("Erreur")
        #dimensions x sur y
        self.root.geometry("%dx%d"%(dim_x,dim_y))
        #le message a afficher
        Label(self.root,text=message).pack()
        #le bouton pour detruire la fenetre
        Button(self.root,text="OK",width=10,command=lambda:self.root.destroy()).pack()
        self.root=mainloop()

#partie graphique générale
class Graphique:
    
    #Cette fonction est activé quand on clique sur un mot du texte : on lance une recherche de suggestions
    def suggestions(self,mot):
        #on vide la liste des suggestions du mot précédent
        self.liste_suggestions.delete(0,END)
        #on recherche des suggestions pour le nouveau mot
        afficher_suggestions(mot)
        #si on ne trouve pas de suggestions -> message d'erreur
        if SUGG.get(mot)==None:
            pop_up("pas de suggestions pour ce mot.\n\n\n")
        else:
            #sinon on affiche un par un les élements à sugger dans une liste
            liste=SUGG[mot].split(" ")
            for i in liste:
                self.liste_suggestions.insert(END,i)

    #Cette fonction est activé quand on clique sur le bouton Validé
    #Il s'agit ici d'appliquer la correction souhaité
    def appliquer_correction(self):
        global RESULTAT
        #si la longueure de la chaine de caractere dans Entry (dans laquel l'utilisateur entre une correction) dépasse 0, on applique cette correction
        if len(self.utilisateur.get())>0:
            self.correction=self.utilisateur.get()
        #si le nombre d'elements dans la liste de suggestions depasse 0
        elif self.liste_suggestions.size()>0:
            #si l'utilisateur n'a pas selectionné de mot dans la liste on envoit une fenetre d'erreur
            if len(list(self.liste_suggestions.curselection()))==0:
                pop_up("Vous devez faire un choix de correction\n\n\n",250)
            #sinon on appliquer la correction a partir de la selection dans la liste
            else:
                self.correction=self.liste_suggestions.get(self.liste_suggestions.curselection()[0])
        #si l'utilisateur n'a pas fait de choix on arrete la fonction sur une erreur
        else:
            pop_up("Vous devez faire un choix de correction\n\n\n",250)
            return ;
        #si il n'y a pas d'erreur, on recherche dans toutes les mots de toutes les lignes les occurences du mot a corriger
        for i in range(len(self.texte)):
            for j in range(len(self.texte[i])):
                #si on l'a trouvé on applique la correction
                if self.texte[i][j]==self.a_corriger:
                    RESULTAT[self.correction]="1"
                    self.texte[i][j]=self.correction
                    #si l'utilisateur n'a pas cliqué sur le checkbutton "toutes les occurences"
                    if self.valeur_check_occurences.get()==0:
                        self.recharger()
                        return ;
        #on recharge le texte
        self.recharger()

    #destruction du canvas et remise en route
    def recharger(self):
        global RESULTAT
        #on vide le canvas dans lequel on a placé le texte (ce qui a pour effet de le supprimer), c'est d'ailleur l'interet d'utiliser un canvas car on ne peut pas supprimer le contenu d'une frame  
        self.c.destroy()
        #on redeclare le widget avec le scroll (yscroll = scroll horizontal)
        self.c = Canvas(self.Frame_texte,yscrollcommand=self.scroll.set)
        #on place le canvas sur la grille
        self.c.grid(row=0, column=0, sticky="news")
        #on appliquer l'evenement de scroll ... quand on scroll (oui ce n'est pas fait automatiquement)
        self.scroll.config(command=self.c.yview)
        #ça j'ai jamais compris a quoi ça servait, mais si on le met pas tout fout le camp 
        self.Frame_texte.grid_rowconfigure(0, weight=1)
        self.Frame_texte.grid_columnconfigure(0, weight=1)
        #la frame dans lequel on va placer le texte
        self.fr = Frame(self.c)
        #ici chaque ligne du texte correspond a une petite frame que l'on va packer dans Frame_texte
        for ligne in self.texte:
            test=Frame(self.fr)
            #j'utilise cette variable pour eviter qu'un mot ne depasse pas la longueur de la Frame
            compte_lettre=0
            for i in range(len(ligne)):
                #on "saute une ligne" (on redeclare une frame dans le cas present) si le mot est trop long pour etre affiché dans la page (en gros si on arrive dans cette condition, c'est qu'on est arrivé en bout de page
                if(compte_lettre>40):
                    test.pack()
                    compte_lettre=0
                    test=Frame(self.fr)
                #si le mot est défini comme n'étant pas dans le dictionnaire on l'affiche sous l'aspect d'un bouton
                if ligne[i]=="essais":
                    print(RESULTAT)
                if(RESULTAT[sub("[\?!:\.,]","",ligne[i])]=="0"):
                    Button(test,text=ligne[i],command=lambda mot=ligne[i]: self.selection(mot)).grid(row=0,column=i)
                else:
                #sinon sous la forme d'un label
                    Label(test,text=ligne[i]).grid(row=0,column=i)
                compte_lettre+=len(ligne[i])
            test.pack()
        
        #on fait en sorte que fr agisse toujours comme une frame dans le canvas (car le canvas fige ce qu'il y a a l'interieur, et donc si on n'utilise pas cette methode, les boutons des frames seront figés et donc non cliquables
        #maj du canvas
        self.c.create_window(0, 0,  window=self.fr)
        #maj du frame (toujours pour les boutons)
        self.fr.update_idletasks()
        #maj du scroll
        self.c.config(scrollregion=self.c.bbox("all"))
    
    def selection(self,mot):
        self.a_corriger=mot
        self.suggestions(mot)

    
    def __init__(self):
        self.texte=TEXTE
        self.correction=""
        self.a_corriger=""
        self.fenetre=Tk()
        self.valeur_check_occurences=IntVar()
        
        self.fenetre.resizable(width=False, height=False)
        self.fenetre.title("Correcteur")
        
        self.Frame_texte = Frame(self.fenetre)
        self.scroll = Scrollbar(self.Frame_texte, orient=VERTICAL)
        self.scroll.grid(row=0, column=1, sticky=N+S)

        #cette partie est expliqué dans la fonction rechargé
        self.c = Canvas(self.Frame_texte,yscrollcommand=self.scroll.set)
        self.c.grid(row=0, column=0, sticky="news")
        self.scroll.config(command=self.c.yview)
        self.Frame_texte.grid_rowconfigure(0, weight=1)
        self.Frame_texte.grid_columnconfigure(0, weight=1)

        self.fr = Frame(self.c)
        for ligne in self.texte:
            test=Frame(self.fr)
            compte_lettre=0
            for i in range(len(ligne)):
                if(compte_lettre>40):
                    test.pack()
                    compte_lettre=0
                    test=Frame(self.fr)
                if(RESULTAT[sub("[\?!:\.,]","",ligne[i])]=="0"):
                    Button(test,text=ligne[i],command=lambda mot=ligne[i]: self.selection(mot)).grid(row=0,column=i)
                else:
                    Label(test,text=ligne[i]).grid(row=0,column=i)
                compte_lettre+=len(ligne[i])
            test.pack()
        self.c.create_window(0, 0,  window=self.fr)
        self.fr.update_idletasks()
        self.c.config(scrollregion=self.c.bbox("all"))

        #dans cette frame on va afficher la liste des suggestions, l'Entry de l'utilisateur, le checkbutton de toutes les occurences, et les boutons valider et quitter
        self.Frame_actions=Frame(self.fenetre)
        #liste des suggestions
        self.liste_suggestions=Listbox(self.Frame_actions)
        #Entry de l'utilisateur
        self.utilisateur=Entry(self.Frame_actions)
        #toutes les occurences
        self.les_occurences=Checkbutton(self.Frame_actions,text="Toutes les occurences",variable=self.valeur_check_occurences)
        self.valider=Button(self.Frame_actions,text="Valider",command=lambda : self.appliquer_correction())
        self.quitter=Button(self.Frame_actions,text="Quitter",command=lambda : self.fenetre.destroy())
                
        #affichage des elements
        self.Frame_texte.pack(side=LEFT)
        self.Frame_actions.pack(side=TOP)
        self.liste_suggestions.pack()
        Label(self.Frame_actions,text="Correction\npersonnalisé").pack()
        self.utilisateur.pack()
        self.les_occurences.pack()
        self.valider.pack()
        self.quitter.pack()
        self.fenetre.mainloop()
        
if len(sys.argv)==3:
    print("Mode Recherche")
    correction()
    print()
elif sys.argv[3]=="-s":
    print("Mode Suggestions")
    correction(True)
    print()
elif sys.argv[3]=="-i":
    print("Mode Correction")
    correction(True,True)
    texte="\n".join(" ".join(i) for i in TEXTE)
    for i in CHOIX:
        texte=texte.replace(i,CHOIX[i])
    open((len(sys.argv)==5 and sys.argv[4] or sys.argv[2]),"w").write(texte)
    utilisateur=set(open("user").read().split("\n"))
    new = set(list(map(lambda x:CHOIX[x],CHOIX)))
    open("user","w").write("\n".join(list((new | utilisateur) - set(DICTIONNAIRE))))
elif sys.argv[3]=="-g":
    print("Mode Graphique")
    correction()
    p = Graphique()
else:
    print("??ERREUR??")
