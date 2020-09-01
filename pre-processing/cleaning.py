import unicodedata

from bs4 import BeautifulSoup
import sqlite3
import requests
import re
import json
import pandas as pd
import os
import pkg_resources
import nltk
from symspellpy.symspellpy import SymSpell
from symspellpy.symspellpy import SymSpell, Verbosity  # import the module


def load_dictionnary(dict_path):
    with open(dict_path) as f :
        L = f.readlines()
    words = []
    for i in L:
        words.append(i.split(" ")[0])
    return words


def load_lexique(lexique_path):
    with open(lexique_path) as f:
        L = f.readlines()
    words = []
    for i in L:
        words.append(i.split("\t")[0])
    return words


class Cleaner:
    def __init__(self, directory, lexique_path, dict_path):
        self.directory = directory
        self.dict_path = dict_path
        self.stopwords = list(nltk.corpus.stopwords.words('french'))
        self.lexique_path = lexique_path
        self.words = load_dictionnary(self.dict_path) + self.stopwords + load_lexique(self.lexique_path)
        self.corrected = {}
        
        self.max_edit_distance_dictionary = 2
        self.prefix_length = 7
        self.sym_spell = SymSpell(self.max_edit_distance_dictionary, self.prefix_length)
        self.dictionary_path = "../ressources/fr-100k.txt"
        self.sym_spell.load_dictionary(self.dictionary_path, term_index=0, count_index=1)
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
                m1 = re.match(r"(^.*?(La Cour,|L(A|À|a) COUR)(?! DE)(.+)$|^J\s?U\s?G\s?E\s?M\s?E\s?N\s?T\.?\s?$|^A\s?R\s?R\s?(Ê|E)\s?T\s?\.?\s?$)", string)
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

    def save(self, df, ark, year):
        df.to_csv(f"{self.directory}/{year}/{ark}.csv", encoding="utf-8", sep = ";")
        pass
    def postProcess(self, df, ark, year, recceuil):
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
        
        # add link
        df["lien"]  = "https://gallica.bnf.fr/ark:/12148/" + ark+"/f"
        df["lien"] = df["lien"] + df.page.map(str) +".image"

        df["id"] = "" + str(year) + str(recceuil) + df.index.map(str)
        df.index = df.id
        return df  
    def spell_check(self, df):
        df["arrêt"] = df["arrêt"].apply(self.correct)
        return df
    def correct(self,text):
        ntokens= []
        tokens = re.split('\s|,|\.|;|—|–|-|–|–|\n|:|\!|\?',text)
        for t in tokens:
            if(str(t).lower().isalpha() and not str(t).lower() in self.words and not str(t)[0].isupper()):
                if str(t) in self.corrected:
                    nt = self.corrected[t]
                else:
                    nt = t
                    suggestion = self.sym_spell.lookup_compound(t, 2)
                    if len(suggestion)> 0 : 
                        nt = suggestion[0].term
                    
                    self.corrected[t] = nt
                ntokens.append(nt)

            else:
                ntokens.append(t)
        return " ".join(ntokens)
                
             
        
                
                 
                
        
        




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
