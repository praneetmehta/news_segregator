#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 20:07:49 2017

@author: praneet
"""


import pickle
import re

def correct(s):
        s = re.sub('\s\W',' ',s)
        s = re.sub('\W\s',' ',s)
        s = re.sub("[^a-zA-Z']",' ', s)
        s = re.sub('\s+',' ',s)
        return s
        
vectorizer,assignment,kmeans = pickle.load(open('../pickel/newssort', 'rb'))
def predict(text):
        return assignment[kmeans.predict(vectorizer.transform([correct(text)]))[0]] 
