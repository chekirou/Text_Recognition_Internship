import re
import os

"""
Extrait bien tous les renseignements mais passe a coté de certains arrêts, surement parce que la partie qui extrait la date etc.. ne remplis pas encore
tous les cas particuliers possibles, la partie qui extrait le contenu des arrêts fonctionne bien cependant comme on peut le voire dans extraction 3.
"""

with open("19110105.txt") as file:
    content = file.read()
    L = re.findall("(((COUR|TRIBUNAL).*?) (Présidence de ((.*?).)) (Audience du ((\d+) (\w+) (\d+\.)))) (.*?) « ((La Cour|Le Tribunal) ; (.*?))\. » (.*?) —",content)
    for i in L:
        print("====")
        print(i[1])
        print(i[5])
        print(i[6])
        print(i[14])