# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 03:54:48 2017

@author: praneet
"""
from os import listdir
import numpy as np
from functools import reduce

def filereader(folders,parent):
    
    files = np.array([[open(parent+folder+'/'+f).read() for f in listdir(parent+folder)] for folder in folders])   
    text =  np.array(reduce(lambda x,y:x+y,[i for i in files]))
    text =  text.reshape(text.shape[0],)
    return text
