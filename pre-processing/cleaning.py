import unicodedata

from bs4 import BeautifulSoup
import sqlite3
import requests
import re
import json
import pandas as pd

class Cleaner:
    def __init__(self, directory):
        self.directory = directory
        pass
    def extract(self, file):
        soup = BeautifulSoup(file , "html.parser")
        df = pd.DataFrame(columns=["page", "arrêt", "date", "juridiction"])
        Decision, notes, page, new_page = False, False, 0, True
        for tag in soup.body : 
            if tag.name == "hr":
                page += 1
                notes = False
                new_page  = True
            if page > 3 and tag.name == "p" and tag.string is not None and not new_page:
                m1 = re.match(r".*?LA COUR(.+)", tag.string)
                m2 = re.match(r"^Du(.+?\d{3}.+?)—(.+?)—.+$", tag.string ) 
                if not Decision and m1:
                    Decision = True
                    text = m1.groups()[0]
                    First_page = page
                elif Decision and m2 :
                    Decision = False
                    date = m2.groups()[0]
                    juridiction = m2.groups()[1]
                    df = df.append({'page' : First_page, 'arrêt' : text , "date": date, "juridiction" : juridiction},ignore_index=True)
                    text = ''
                elif not notes:
                    if not re.match(r"^\(\d*\).+$", tag.string):
                    	if Decision:
                        	text+= tag.string + "\n"
                    else:
                        notes = True
                else:
                    pass
            else :
                new_page = False
        return df
    def save(self, df, ark):
        df.to_csv(f"{self.directory}/{ark}.csv", encoding="utf-8")
        pass
        




def clean(file,ark, index_directories= "test"):
    """function to clean with a regex : a bit faster but with erros on the pages """
    soup = BeautifulSoup(file , "html.parser")
    count = 1
    df = pd.DataFrame(columns=["page", "arrêt", "date", "juridiction"])
    text = soup.text
    complete = re.findall(r"LA COUR(;|:).+?([A-Za-z].+?)\. Du(.+?(\d{3}|\d{2}.\d).+?)\.?\s?(—|-)(.+?)\.?(—|,)", text)
    end = re.findall(r"(.+)Du(.+?(\d{3}|\d{2}.\d).+?)\.?\s?(—|-)(.+?)\.?(—|,)")
    for _, arret, date, _,_,region,_ in m:
        df = df.append({'page' : page, 'arrêt' : arret , "date": date, "juridiction" : region},ignore_index=True)
    return df
