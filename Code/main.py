# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import reader as rd
import lemmatizer as lm
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

folders = ['business','entertainment','politics','sport','tech']
text = pd.Series(rd.filereader(folders, '../train/'))
stopwords_utf = [word.decode('utf-8') for word in stopwords.words('english')]
#lemm_text = lm.wordtokenize(text)
#clean_text = lm.clean_text(lemm_text,"[^a-zA-Z']")

vectorizer = TfidfVectorizer(lowercase=True, stop_words=stopwords_utf)

text_vector = vectorizer.fit_transform(text)



kmeans = KMeans(n_clusters=5)
kmeans.fit(text_vector)
#%%

text_test = (rd.filereader(['tech'], '../train/'))
text_test = pd.Series([re.sub("[^a-zA-Z]"," ",test) for test in text_test])
x = range(0,text_test.shape[0])
y = [kmeans.predict(a) for a in vectorizer.transform(text_test)]
plt.scatter(x,y)

#entertainment = 0
#sport = 2
#tech = 3
#business = 4