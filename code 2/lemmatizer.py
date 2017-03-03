# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 16:35:05 2017

@author: praneet
"""

from nltk import pos_tag, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

lemmatizer = WordNetLemmatizer()

def lemmatize(token, tag):  
    if tag[0].lower() in ['n','v']:
        return lemmatizer.lemmatize(token, tag[0].lower())
    return token

def wordtokenize(corpus):   
    corpus = [unicode(t, errors='ignore') for t in corpus]
    tagged = [pos_tag(word_tokenize(document)) for document in corpus]
    lemmatized = [[lemmatize(token, tag) for token, tag in document]for document in tagged]
    joined = [(' ').join(text) for text in lemmatized]
    return joined

