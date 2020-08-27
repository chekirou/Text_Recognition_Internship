import unicodedata

from bs4 import BeautifulSoup
import sqlite3
import requests
import re
import json
import pandas as pd

class Scrapper:
    @staticmethod
    def get_arks(year):
        """ returns set of arks for a given year"""
        url_base = "https://gallica.bnf.fr/ark:/12148/cb34363188x/date"+str(year)+"0101"
        req = requests.get(url_base, headers={'User-Agent': 'Mozilla/5.0'})
        p = req.content
        L = re.findall(r"https://gallica.bnf.fr/ark:/(\d*/(bpt\w*))?",str(p))
        S = set()
        for i in L:
            if(i[1] != ""):
                S.add(i[1])
        return S
    @staticmethod
    def get_pagination(ark):
        """fonction qui renvoie le nombre de pages d'un documents"""
        req = requests.get("https://gallica.bnf.fr/services/Pagination?ark=" + ark)
        p = req.content
        pages = re.search(r"<nbVueImages>(\d*)</nbVueImages>", str(p))
        return pages.groups()[0]
    @staticmethod
    def get_page(ark, page, number = 1):
        """ renvoie une page specifique"""
        req = requests.get(f"https://gallica.bnf.fr/ark:/12148/{ark}/f{page}n{number}.texteBrut")
        return req.content
    @staticmethod
    def get_document(ark, mode = "texteBrut"):
        """renvoie un document dans le format souhaitee """
        req = requests.get("https://gallica.bnf.fr/ark:/12148/"+ark+"."+ mode)
        return req.content
    