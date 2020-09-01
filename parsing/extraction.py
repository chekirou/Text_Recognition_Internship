import re
import os

with open("parsed/19110101.txt") as file:
    content = file.read()
    #L = re.findall("«(.*?)»",content)
    L = re.findall("((COUR|TRIBUNAL).*?) Présidence de (.*?) Audience du ((\d+) (\w+) (\d+\.)) ([A-Z—,.\(\)0-9 ■'\-É]+)[A-Z].*?«(.*?)»", content)
    for i in L:
        print("ARRET EXTRAIT -- ")
        print("-------------------")
        print("Endroit : ",i[0])
        print("Le gars : ",i[2])
        print("Date : ",i[3])
        print("Rubriques : ",i[7])
        print("Contenu : ",i[-1])
        print("-------------------")


