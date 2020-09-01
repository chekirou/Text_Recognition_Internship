import re

import requests
from bs4 import BeautifulSoup


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import argparse


def SoupeURL(URL):
    req = requests.get (URL , headers={'User-Agent': 'Mozilla/5.0'})
    p = req.content
    B = BeautifulSoup (p , "lxml")
    return B


def Debaliser(string):
    ch = str(string)
    ch = ch.replace("<br/>","")
    ch = re.sub ("<.*?>" ," ",str (ch))
    ch = re.sub("^ *","",str(ch))
    ch = re.sub("^\s*","",str(ch))
    ch = ch.rstrip()
    return ch

"""
ça parcours entre les deux année avec comme limite un nombre de gazettes.
ça retourne la liste des chemins ou y'a les pdf
"""
def parcourir_entre_deux(annee1,annee2, nb=200):
    cpt = 0
    cpt = cpt + 1
    fichiers = []
    for annee in range(annee1,annee2):
        for mois in range(1,13):
            for jour in range(1,32):
                jour_f = str(jour)
                if(len(jour_f) == 1):
                    jour_f = "0"+jour_f
                mois_f = str(mois)
                if(len(mois_f) == 1):
                    mois_f = "0" + mois_f
                date = str(annee) + mois_f + jour_f
                url = "http://www.enap.justice.fr/ARCHIVE/"+date+".pdf"
                req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                if(req.status_code == 200):
                    f = open("downloads/"+date+".pdf","wb")
                    fichiers.append("downloads/"+date+".pdf")
                    f.write(req.content)
                if(len(fichiers) == nb):
                    return fichiers

def pdf2xt(path):
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    device = TextConverter(rsrcmgr, retstr)
    with open(path, "rb") as fp:  # open in 'rb' mode to read PDF bytes
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, check_extractable=True):
            interpreter.process_page(page)
        device.close()
        text = retstr.getvalue()
        retstr.close()
    return text

import os


if __name__ == '__main__':

    if not os.path.exists("parsed"):
        os.mkdir("parsed")
        print("Directory ", "parsed", " Created ")


    if not os.path.exists("downloads"):
        os.mkdir("downloads")
        print("Directory ", "downloads", " Created ")

    #Je teste sur un seul journal
    pdf_path = parcourir_entre_deux(1911, 1920, 1)[0]
    print(pdf_path)
    content = (pdf2xt(pdf_path))
    f = open("parsed/"+pdf_path.split("/")[-1].split(".")[0]+".txt","wb")
    f.write(content)