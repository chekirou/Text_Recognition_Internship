import re
import os
import requests
import pandas as pd
from Gazette.parsing import  parse_year, pdf2xt
import numpy as np

def extract_arrets(file_path):
    arrets = []
    with open(file_path) as file:
        content = file.read()
        L = re.findall("« ((La Cour|Le Tribunal) ; (.*?))\. » (.*?) —", content)
        for i in L:
            arrets.append(i[0])
    return arrets

def extract_datas(file_path):
    with open(file_path) as file:
        content = file.read()
        datas = []
        L = re.findall("(Audience du (.*?)\.(.*?) « ((La Cour|Le Tribunal) ; (.*?))\. » (.*?)) —",
                       content)
        for i in L:
            print("==================")
            for k, j in enumerate(i):
                print(k, "==>", j)
            print("==================")
            arret, president, date = i[4], i[1], i[2]
            datas.append((arret,president,date))
        return datas

def extract_all(file_path):
    with open(file_path) as file:
        datas = []
        content = file.read()
        L = re.findall(
            "(((COUR|TRIBUNAL).*?) (Présidence de ((.*?).)) (Audience du ((\d+) (\w+) (\d+\.)))) (.*?) « ((La Cour|Le Tribunal) ; (.*?))\. » (.*?) —",
            content)
        for i in L:
            juridiction = (i[1])
            president = (i[5])
            date = (i[6]).replace("Audience du ","")
            arret = (i[14])
            datas.append((president,date,juridiction,arret))
        return datas

def extract_from_txt(content):
    datas = []
    L = re.findall(
        "(((COUR|TRIBUNAL).*?) (Présidence de ((.*?).)) (Audience du ((\d+) (\w+) (\d+\.)))) (.*?) « ((La Cour|Le Tribunal) ; (.*?))\. » (.*?) —",
        content)
    for i in L:
        juridiction = (i[1])
        president = (i[5])
        date = (i[6]).replace("Audience du ", "")
        arret = (i[14])
        datas.append([president, date, juridiction, arret])
    return datas



def extract(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        datas = []
        text = file.read()

    df = pd.DataFrame(columns=[ "arrêt", "date", "juridiction"])
    f = re.findall(r"(?<!DU)(?<!«)((?: TRIBUNAL| COUR).+?) du ((?:\S+ ){3})", str(text))
    s = re.split(r"(?<!DU)(?<!«)(?:(?: TRIBUNAL| COUR).+?) du (?:(?:\S+ ){3})", str(text))
    for (cour, date), string in zip(f, s[1:]):
      m = re.findall(r"(« (?:La (?:C|G)our|Le Tribunal).+?)(?:»|[A-Z]{3})", string)
      for message in m:
        df = df.append({ 'arrêt' : message , "date": date, "juridiction" : cour},ignore_index=True)
    df["juridiction"] = df["juridiction"].apply(lambda x : re.split(r"\.|\(", x)[0] )
    df["arrêt"] = df["arrêt"].apply(lambda x : re.split(r"OBSERVATIONS", x)[0] )
    df["date"] = df["date"].apply(lambda x : re.split(r"\.", x)[0] )
    return df

def get_annee(annee):
    annee = str(annee)
    if not os.path.exists("cache/"):
        os.mkdir("cache/")
        print("Directory ", "cache/" , " Created ")
    if not os.path.exists("cache/"+annee):
        os.mkdir("cache/"+annee)
        print("Directory ", "cache/"+annee , " Created ")
    DF = pd.DataFrame(columns=[ "arrêt", "date", "juridiction", "lien", "id"])
    for mois in range(1, 13):
        for jour in range(1, 32):
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
                url = "http://data.decalog.net/enap1/liens/Gazette/ENAP_GAZETTE_TRIBUNAUX_" + date + ".pdf"
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
    DF.to_csv(f"cache/{annee}/Gazette_des_tribunaux.csv", encoding="utf-8", sep = ";")
