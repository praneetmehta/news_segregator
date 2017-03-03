#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 01:06:26 2017

@author: praneet
"""

def assign(categories, parent):
    for i in categories:
        test_text = pd.Series(rd.filereader([i],parent))