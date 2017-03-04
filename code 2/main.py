# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 03:45:45 2017

@author: praneet
"""
from __future__ import division
from sklearn.feature_extraction.text import  TfidfVectorizer
import reader as rd
import re
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import lemmatizer as lm
import pickle

#%%
def correct(s):
        s = re.sub('\s\W',' ',s)
        s = re.sub('\W\s',' ',s)
        s = re.sub("[^a-zA-Z']",' ', s)
        s = re.sub('\s+',' ',s)
        return s
#meandistortions.append(sum(np.min(cdist(text_vector, kmeans.cluster_centers_, 'euclidean'), axis=1))/text_vector.shape[0])
#%%
def plot(name):
    text_test = (rd.filereader([name], '../train/'))
    text_test = pd.Series([correct(test) for test in text_test])
    x = range(0,text_test.shape[0])
    y = [kmeans.predict(a) for a in vectorizer.transform(text_test)]
    plt.scatter(x,y)

#%%
def assign():   
    assignment = []
    possible = []
    true_count = 0
    for i in categories:        
        test_text = rd.filereader([i],'../train/')
        test_text = pd.Series([correct(test) for test in test_text])
        val = [kmeans.predict(a)[0] for a in vectorizer.transform(test_text)]
        count = Counter(val)
        print(count.most_common(3))
        if count.most_common(1)[0][0] in possible:
            assignment.append((count.most_common(2)[1][0],i))
            true_count += count.most_common(2)[1][1]
            possible.append(count.most_common(2)[1][0])
        else:
            assignment.append((count.most_common(1)[0][0],i))  
            true_count += count.most_common(1)[0][1]
            possible.append(count.most_common(1)[0][0])
    accuracy = float(((true_count)/shape)*100)
    return dict(assignment), accuracy, true_count
     
#%%
def predict():
        text = open('./test.txt','r').read()
        return assignment[kmeans.predict(vectorizer.transform([correct(text)]))[0]] 
         
#%%
categories = ['business','entertainment','politics','sport','tech']
text = pd.Series(rd.filereader(categories, '../train/'))
shape = text.shape[0]
text = [correct(t) for t in text]
#text = lm.wordtokenize(text)
vectorizer = TfidfVectorizer(stop_words='english', encoding='iso-8859-1', ngram_range=(1,2))
text_vector = vectorizer.fit_transform(text)
kmeans = KMeans(n_clusters=5)
kmeans.fit(text_vector)
assignment = []
assignment, accuracy, true_count = assign()
print (assignment)

#%%
pickle.dump([vectorizer,assignment,kmeans], open('../pickel/newssort', 'wb'))
