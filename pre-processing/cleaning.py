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
        Decision, notes, page, new_page, new_decision, count = False, False, 0, True, False,1
        for tag in soup.body :
            if count == 15:
                count = 0
                Decision = False
            new_decision = False
            string = tag.get_text()
            if tag.name == "hr":
                page += 1
                notes = False
                new_page  = True
            if tag.name == "p" and string is not None and not new_page:
                m1 = re.match(r"(^.*?(La Cour,|L(A|À|a) COUR)(?! DE)(.+)$|^JUGEMENT\.?\s?$|^A\s?R\s?R\s?(Ê|E)\s?T\.\s?$)", string)
                m2 = re.match(r"(.*?)D(u|û|ù)(.+?)(—|–|-|–|–)(.+)", string ) 
                
                if not Decision and m1:
                    Decision = True
                    text = ""
                    count = 1
                    if m1.groups()[3] != None:
                        text = str(m1.groups()[3])
                    First_page = page
                    new_decision = True
                if Decision and m2:
                    if count < 15:
                        if(new_decision):
                            text =m2.groups()[0]
                        else:
                            text += m2.groups()[0]
                        date = m2.groups()[2]
                        juridiction = m2.groups()[4]
                        df = df.append({'page' : First_page, 'arrêt' : text , "date": date, "juridiction" : juridiction},ignore_index=True)
                    Decision = False
                    text = ''
                elif not notes and Decision and not new_decision:
                    if not re.match(r"^\(\d*\).+$", string):
                        count +=1
                        text+= string + "\n"
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
    def postProcess(self, df):
        # fix mix date-juridiction
        Rows_contains_ = df['date'].str.contains(r"(—|–|-)")
        for i, row in df[Rows_contains_].iterrows():
            m = re.search(r"(.+?)(—|–|-|—)(.+)(—|–|-|—)?.*", row["date"] )
            if m:
                df.at[i, "date"] = m.groups()[0]
                df.at[i, "juridiction"] = m.groups()[2]
        #if still not fixed --> drop them
        Rows_contains_ = df['date'].str.contains(r"(—|–|-)")
        df = df[Rows_contains_ == False]
        # drop date too long
        leng = df["date"].str.len()
        df = df[leng < 25] # drop too long date
        # drop date with no number
        number = df["date"].str.contains("^\D*$")
        df = df[number== False] # drop too long date
        length_decision = df.arrêt.str.len()
        # drop decision too short
        df = df[length_decision > 100]
        # drop juridiction too long
        for i , row in df.iterrows():
            m = re.search(r"(.+?)(—|–|-|—|,|;).*", row["juridiction"] )
            if m:
                df.at[i, "juridiction"] = m.groups()[0]
        
        # process the juridiction
        
        return df              
        
                
              
        
                
                 
                
        
        




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
