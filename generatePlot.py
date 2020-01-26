# -*- coding: utf-8 -*-
"""
MLP:FiM Episode's plot generator based on n-grams

@author: Polonius
"""

import glob
import re
from collections import defaultdict
import random
import os

def generateEpisode():
    #Upload episodes summaries from files
    path=r"episodes\*"
    script=''
    for fn in glob.glob(path):
        with open(fn,'r') as file:
            for line in file:
                script=script+line
    script=script.replace('\n\n', '99999 ')
    
    #Create trigrams list
    words=script.split()           
    trigrams=zip(words,words[1:],words[2:])
    
    #Generate transitions methods:
    #Have 2 previous words -> get a new word
    #Also choose the starting ones
    trigramTransitions=defaultdict(list)
    
    starts=[]
    for prev, current, nextt in trigrams:
        #If it's character name, make it a potential starter
        if re.search("99999",prev):
            starts.append((prev,current))
        #Create transition method
        trigramTransitions[(prev,current)].append(nextt)
    
    #Choose starting words
    prev,current=random.choice(starts)
    result=[current]
    
    #Generate script
    while True:
        nextWords=trigramTransitions[(prev,current)]
        nextt=random.choice(nextWords)
        
        prev,current=current,nextt
        result.append(current)        
        
        #The end of the script - randomly choose the ending part
        if re.search('99999',current) and random.random()<=0.1:
            final=" ".join(result)
            final=final.replace('99999', '\n\n')
            break
    
    try:
        # Create target Directory
        os.mkdir('newEpisodes')
        print("Directory Created") 
    except FileExistsError:
        print("Directory already exists")
    
    #Write script to the file
    with open('newEpisodes/newEpisode.txt','w') as file:
        file.write('%s' % final)
        
    print('New episode created')