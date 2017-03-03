# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 03:45:45 2017

@author: praneet
"""

from sklearn.feature_extraction.text import  TfidfVectorizer
import reader as rd
import re
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
   
#meandistortions.append(sum(np.min(cdist(text_vector, kmeans.cluster_centers_, 'euclidean'), axis=1))/text_vector.shape[0])
#%%
def plot(kmeans, vectorizer, name):
    text_test = (rd.filereader([name], '../train/'))
    text_test = pd.Series([re.sub("[^a-zA-Z]"," ",test) for test in text_test])
    x = range(0,text_test.shape[0])
    y = [kmeans.predict(a) for a in vectorizer.transform(text_test)]
    plt.scatter(x,y)

#%%
def assign(categories, parent, kmeans, vectorizer):
    assignment = []
    possible = []
    for i in categories:
        test_text = rd.filereader([i],parent)
        test_text = pd.Series([re.sub("[^a-zA-Z]"," ",test) for test in test_text])
        val = [kmeans.predict(a)[0] for a in vectorizer.transform(test_text)]
        count = Counter(val)
        print count
        if count.most_common(1)[0][0] in possible:
            assignment.append((count.most_common(2)[1][0],i))
        else:
            assignment.append((count.most_common(1)[0][0],i))            
        possible.append(count.most_common(1)[0][0])
    return dict(assignment)
     
#%%
def predict(assignment, kmeans, vectorizer):
        text = open('./test.txt','r').read()
        return assignment[kmeans.predict(vectorizer.transform([re.sub("[^a-zA-Z]"," ",text)]))[0]] 
         
#%%
categories = ['business','entertainment','politics','sport','tech']
text = pd.Series(rd.filereader(categories, '../train/'))
text = [re.sub('[^a-zA-Z]',' ',t) for t in text]
vectorizer = TfidfVectorizer(stop_words='english', encoding='iso-8859-1', ngram_range=(1,2))
text_vector = vectorizer.fit_transform(text)
kmeans = KMeans(n_clusters=5)
kmeans.fit(text_vector)
assignment = []
assignment = assign(categories, '../train/', kmeans, vectorizer)
print assignment