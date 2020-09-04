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


def get_annee(annee):
    annee = str(annee)
    if not os.path.exists("cache/"):
        os.mkdir("cache/")
        print("Directory ", "cache/" , " Created ")
    if not os.path.exists("cache/"+annee):
        os.mkdir("cache/"+annee)
        print("Directory ", "cache/"+annee , " Created ")
    datas = []
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
                datas = datas + extract_all("tmp.bin")
                data_dict = {
                    "juridiction":[],
                    "date":[],
                    "lien":[],
                    "arret": [],
                }
                for (president,date,juridiction,arret) in datas:
                    data_dict["juridiction"].append(juridiction)
                    data_dict["date"].append(date)
                    data_dict["lien"].append(url)
                    data_dict["arret"].append(arret)
    df = pd.DataFrame(data_dict)
    df.to_csv("cache/"+annee+"/"+date.replace(' ',"")+"csv")

get_annee(1911)