import pandas as pd
import numpy as np
import os
import pkg_resources
import nltk
from symspellpy.symspellpy import SymSpell
from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

dict_path = "../ressources/fr-100k.txt"
stowords = list(nltk.corpus.stopwords.words('french'))
lexique_path = "../ressources/Lexique383.tsv"

def load_dictionnary():
    f = open(dict_path)
    L = f.readlines()
    words = []
    for i in L:
        words.append(i.split(" ")[0])
    return words


def load_lexique():
    f = open(lexique_path)
    L = f.readlines()
    words = []
    for i in L:
        words.append(i.split("\t")[0])
    return words

def spell_correction(texte):
    max_edit_distance_dictionary = 2
    prefix_length = 7
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    dictionary_path = "../ressources/fr-100k.txt"
    bigram_path = pkg_resources.resource_filename(
        "symspellpy", "frequency_bigramdictionary_en_243_342.txt")
    if not sym_spell.load_dictionary(dictionary_path, term_index=0,
                                     count_index=1):
        print("Dictionary file not found")
        return
    if not sym_spell.load_bigram_dictionary(bigram_path, term_index=0,
                                            count_index=2):
        print("Bigram dictionary file not found")
        return
    input_term = texte
    # max edit distance per lookup (per single word, not per whole input string)
    max_edit_distance_lookup = 2
    suggestions = sym_spell.lookup_compound(input_term,
                                            max_edit_distance_lookup)
    # display suggestion term, edit distance, and term frequency
    for suggestion in suggestions:
        print("{}, {}, {}".format(suggestion.term, suggestion.distance,
                                  suggestion.count))
    if(len(suggestions)>0):
        return suggestions[0].term
    else:
        print("error with : ",texte)
        return texte

#print(spell_correction("bonjour"))

df = pd.read_csv("/home/mohamed/Bureau/Projets/Projet_Dice_Battle/Internship/cache/bpt6k5802646m.csv")


words = load_dictionnary() + stowords + load_lexique()
for arret in df["arrêt"]:
    ntokens = []
    tokens = arret.split(" ")
    for t in tokens:
        if(str(t).lower().isalpha() and not str(t).lower() in words and not str(t)[0].isupper()):
            nt = spell_correction(t)
            print(t + " ->" + nt)
            ntokens.append(nt)
        else:
            ntokens.append(t)

