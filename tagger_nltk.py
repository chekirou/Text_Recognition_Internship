import nltk #import the natural language toolkit library
from nltk.stem.snowball import FrenchStemmer #import the French stemming library
from nltk.corpus import stopwords #import stopwords from nltk corpus
import re #import the regular expressions library; will be used to strip punctuation
from collections import Counter #allows for counting the number of occurences in a list
from stop_words import get_stop_words
nltk.download("stopwords")


import nltk #import the Natural Language Processing Kit
from nltk.tag.stanford import StanfordPOSTagger
nltk.download('punkt')

#reading in the raw text from the file

def read_raw_file(path):
    '''reads in raw text from a text file using the argument (path), which represents the path/to/file'''
    f = open(path,"r") #open the file located at "path" as a file object (f) that is readonly
    raw = f.read().decode('utf8') # read raw text into a variable (raw) after decoding it from utf8
    f.close() #close the file now that it isn;t being used any longer
    return raw

def get_tokens(raw,encoding='utf8'):
    '''get the nltk tokens from a text'''
    tokens = nltk.word_tokenize(raw) #tokenize the raw UTF-8 text
    return tokens

def get_nltk_text(raw,encoding='utf8'):
    '''create an nltk text using the passed argument (raw) after filtering out the commas'''
    #turn the raw text into an nltk text object
    no_commas = re.sub(r'[.|,|\']',' ', raw) #filter out all the commas, periods, and appostrophes using regex
    tokens = nltk.word_tokenize(no_commas) #generate a list of tokens from the raw text
    text=nltk.Text(tokens,encoding) #create a nltk text from those tokens
    return text

def get_stopswords(type="nltk"):
    raw_stopword_list = []
    if(type=="nltk"):
        raw_stopword_list = stopwords.words('french') #create a list of all French stopwords
    elif(type=="default"):
        raw_stopword_list = get_stop_words("fr")
    return raw_stopword_list

def filter_stopwords(text,stopword_list):
    '''normalizes the words by turning them all lowercase and then filters out the stopwords'''
    words=[w.lower() for w in text] #normalize the words in the text, making them all lowercase
    filtered_words = []
    for word in words:
        if word not in stopword_list and word.isalpha() and len(word) > 1:
            filtered_words.append(word)
    filtered_words.sort()
    return filtered_words

def stem_words(words):
    '''stems the word list using the French Stemmer'''
    #stemming words
    stemmed_words = [] #declare an empty list to hold our stemmed words
    stemmer = FrenchStemmer() #create a stemmer object in the FrenchStemmer class
    for word in words:
        stemmed_word=stemmer.stem(word) #stem the word
        stemmed_words.append(stemmed_word) #add it to our stemmed word list
    stemmed_words.sort() #sort the stemmed_words
    return stemmed_words


def sort_dictionary(dictionary):
    '''returns a sorted dictionary (as tuples) based on the value of each key'''
    return sorted(dictionary.items(), key=lambda x: x[1], reverse=True)


def normalize_counts(counts):
    total = sum(counts.values())
    return dict((word, float(count) / total) for word, count in counts.items())

import nltk
from nltk.tag.stanford import StanfordPOSTagger
root_path="/home/mohamed/PycharmProjects/Receuil_Scrapper/"
pos_tagger = StanfordPOSTagger(root_path + "models/french-ud.tagger", root_path + "stanford-postagger.jar",encoding='utf8') #instance de la classe StanfordPOSTagger en UTF-8
def pos_tag(sentence):
    tokens = nltk.word_tokenize(sentence) #je transforme la phrase en tokens => si vous avez un texte avec plusieurs phrases, passez d'abord par nltk pour récupérer les phrases
    tags = pos_tagger.tag(tokens) #lance le tagging
    return tags


