ecrire = lambda fichier,a_ecrire:open(fichier,"w").write("\n".join(a_ecrire))
lines=sorted(open("mots","r").read().split())
ecrire("aux",lines)
#ecrire("lettres",list(map(lambda x:x[0]+":"+str(x[1]),sorted(dict([(lines[i][:2],i) for i in range(len(lines))]).items()))))
