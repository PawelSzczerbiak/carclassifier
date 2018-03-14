from sklearn.feature_extraction.text import HashingVectorizer
import re
import os
import pickle

cur_dir = os.path.dirname(__file__)
stop = pickle.load(open(
                os.path.join(cur_dir, 
                'pkl_objects', 
                'stopwords.pkl'), 'rb'))

endings = pickle.load(open(
                os.path.join(cur_dir, 
                'pkl_objects', 
                'endings.pkl'), 'rb'))

polish_letters = [
    ('ą','a'), ('ć','c'), ('ę','e'), ('ł','l'), ('ń','n'), 
    ('ó','o'), ('ś','s'), ('ź','z'), ('ż','z')]

def fetch_important(text):
    emoticons = re.findall('[:;=]-?[()DPp]', text)
    emoticons = [e.replace('-','') for e in emoticons]
    rates = re.findall('(\d+/\d+|\d+%)', text)
    return emoticons + rates

def preprocessor(text):
    text = re.sub('\W+', ' ', text)
    text = re.sub('[\w]*\d+[\w]*', '', text)
    text = text.lower()
    for (i, j) in polish_letters:
        text = re.sub(i, j, text)
    text = re.sub('(^|\s)(nie)\s+', ' nie', text)
    return text

def remove_endings(word):
    for ending in endings:
        word = re.sub(ending+'$','', word)
    return word

def tokenizer(text):
    important = fetch_important(text)
    processed = preprocessor(text)
    words = [w for w in processed.split() if len(w) > 1 and w not in stop]
    tokens = [remove_endings(w) for w in words]
    return tokens + important

vect = HashingVectorizer(decode_error='ignore',
                         n_features=2**21,
                         preprocessor=None,
                         tokenizer=tokenizer)