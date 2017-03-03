# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:27:40 2017

@author: praneet
"""
import numpy as np
from os import listdir

def filereader(folders,parent):
    
    files = np.array([[open(parent+folder+'/'+f).read() for f in listdir(parent+folder)] for folder in folders])   
    text =  np.array(reduce(lambda x,y:x+y,[i for i in files]))
    text = text.reshape(text.shape[0],)
    return text
