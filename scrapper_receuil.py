import unicodedata

from bs4 import BeautifulSoup
import sqlite3
import requests
import re
import json


def SoupeURL(URL):
    req = requests.get (URL , headers={'User-Agent': 'Mozilla/5.0'})
    p = req.content
    B = BeautifulSoup (p , "html.parser")
    return B


def Debaliser(string):
    ch = str(string)
    ch = ch.replace("<br/>","")
    ch = re.sub ("<.*?>" ," ",str (ch))
    ch = re.sub("^ *","",str(ch))
    ch = re.sub("^\s*","",str(ch))
    ch = ch.rstrip()
    return ch


def queryFromYear(year):
    url_base = "https://gallica.bnf.fr/ark:/12148/cb34363188x/date"+str(year)+"0101"
    print(year,"-->",url_base)
    req = requests.get(url_base, headers={'User-Agent': 'Mozilla/5.0'})
    p = req.content
    L = re.findall(r"https://gallica.bnf.fr/(ark:/(\d*)/bpt(\w*))?",str(p))
    S = set()
    for i in L:
        if(i[0] != ""):
            S.add(i[0])
    cpt = 0
    for i in S:
        cpt = cpt + 1
        print(cpt,"--> https://gallica.bnf.fr/"+i+".texteBrut")
        req = requests.get("https://gallica.bnf.fr/"+i+".texteBrut")
        clean_text = BeautifulSoup(req.content, "lxml").get_text()
        f = open("downloads/T"+str(year)+str(cpt)+".txt","w")
        f.write(clean_text)




for i in range(1807,1826):
    queryFromYear(i)