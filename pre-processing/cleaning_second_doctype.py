import re

import requests
from bs4 import BeautifulSoup

from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import argparse
import os
import pandas as pd

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
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams(line_margin=0.1))
    with open(path, "rb") as fp:  # open in 'rb' mode to read PDF bytes
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
        device.close()
        text = retstr.getvalue()
        retstr.close()
    return text


def extract(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        datas = []
        text = file.read()

    df = pd.DataFrame(columns=[ "arrêt", "date", "juridiction"])
    f = re.findall(r"\n((?:TRIBUNAL|COUR).+)", str(text))
    s = re.split(r"\n(?:(?:TRIBUNAL|COUR).+)", str(text))
    for cour, string in zip(f, s[1:]):
      m = re.search(r"\n(?:Audience|Séance) (?:du|des)\s+(.+)", string)
      if m is not None:
        date = m.group(1)
        string = re.sub(r"\x0c.+", "", string)
        a = re.findall(r"(« (?:La (?:C|G)our|Le Tribunal).+?(?:»|\s[A-Z]{3}))", string, re.DOTALL)
        for message in a:
          #splits = re.split(r"»", message)
          #if len(splits) > 1 :
          #  message = "".join(splits[:-1])
          #else:
          #  message = splits[0]
          message = message.replace("\n", " ")
          df = df.append({ 'arrêt' : message , "date": date, "juridiction" : cour},ignore_index=True)
    df["juridiction"] = df["juridiction"].apply(lambda x : re.split(r"\.|\)", x)[0] )
    df["arrêt"] = df["arrêt"].apply(lambda x : re.split(r"OBSERVATIONS", x)[0] )
    df["date"] = df["date"].apply(lambda x : re.split(r"\.", x)[0] )
    df["juridiction"] = df.juridiction.str.replace("(", "")
    return df

def get_annee(annee, directory):
    annee = str(annee)
    if not os.path.exists(f"{directory}/{annee}"):
        os.mkdir(f"{directory}/{annee}")
        print("Directory ", f"{directory}/{annee}" , " Created ")
    DF = pd.DataFrame(columns=[ "arrêt", "date", "juridiction", "lien", "id"])
    for mois in range(1, 13):
        for jour in range(1, 31):
            jour_f = str(jour)
            if (len(jour_f) == 1):
                jour_f = "0" + jour_f
            mois_f = str(mois)
            if (len(mois_f) == 1):
                mois_f = "0" + mois_f
            date = str(annee) + mois_f + jour_f
            url = "http://www.enap.justice.fr/ARCHIVE/" + date + ".pdf"
            print(annee, mois_f, jour_f)
            req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if (req.status_code == 200):
                print(mois,"/",jour)
                f = open("tmp.bin", "wb")
                f.write(req.content)
                f.close()
                content = pdf2xt("tmp.bin")
                f = open("tmp.bin", "wb")
                f.write(content)
                f.close()
                df = extract("tmp.bin")
                df["lien"] = url
                df["id"] = "" + annee +mois_f+jour_f + df.index.map(str)
                print(f"{len(df)} rows found")
                DF = DF.append(df)
            else:
                url = "http://www.enap.justice.fr/ARCHIVE/ENAP_GAZETTE_TRIBUNAUX_" + date + ".pdf"
                req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                if (req.status_code == 200):
                    print(mois,"/",jour)
                    f = open("tmp.bin", "wb")
                    f.write(req.content)
                    f.close()
                    content = pdf2xt("tmp.bin")
                    f = open("tmp.bin", "wb")
                    f.write(content)
                    f.close()
                    df = extract("tmp.bin")
                    df["lien"] = url
                    df["id"] = "" + annee +mois_f+jour_f + df.index.map(str)
                    print(f"{len(df)} rows found")
                    DF = DF.append(df)
    print(f"=========={annee}==============")
    DF.index = DF.id
    print(f"In total {len(DF)} rows found")
    DF.to_csv(f"{directory}/{annee}/BASE2_{annee}.csv", encoding="utf-8", sep = ";")

if __name__ == "__main__":
    for year in range(1870,1900):
        get_annee(year)