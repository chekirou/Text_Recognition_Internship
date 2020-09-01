import re
"""
Extrait juste les arrêts mais marche bien
"""
with open("parsed/19110108.txt") as file:
    content = file.read()
    L = re.findall("« ((La Cour|Le Tribunal) ; (.*?))\. » (.*?) —",content)
    for i in L:
        print(i)