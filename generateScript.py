# -*- coding: utf-8 -*-
"""
MLP Scripts generator based on n-grams

@author: Polonius
"""

import episodesList as ep
from nltk.util import ngrams
from collections import defaultdict
import random
import re

#Get episodes titles
titles=ep.getTitles('episodesList.txt')

#Merge all scripts into one for easier work
script=''
for title in titles:
    title=title.replace('?','')
    title=title.replace(':','-')
    fileName='scripts/'+re.sub(' ','_',title)+'.html'
    with open(fileName,'r') as file:
        for line in file:
            script=script+line

#Create trigrams list
trigramsTmp = ngrams(script.split(), 3)
trigrams=[]
for grams in trigramsTmp:
  trigrams.append(grams)

#Generate transitions methods:
#Have 2 previous words -> get a new word
#Also choose the starting ones
trigramTransitions=defaultdict(list)

finalScript=''
starts=[]
for prev, current, nextt in trigrams:
    #If it's character name, make it a potential starter
    if re.search("<dl><dd><b>",prev):
        starts.append((prev,current))
    #Create transition method
    trigramTransitions[(prev,current)].append(nextt)

#Choose starting words
prev,current=random.choice(starts)
result=[prev,current]

#Generate script
while True:
    nextWords=trigramTransitions[(prev,current)]
    nextt=random.choice(nextWords)
    
    prev,current=current,nextt
    result.append(current)
    
    #The end of script
    if prev=='</dd><dd>[credits]':
        #Shrink the script, so it'll have a show-lenght
        resultTmp=result[:1000]
        resultTmp=resultTmp+result[1000:]
        result=resultTmp
        final=" ".join(result)
        break

#Write script to the file
with open('newScript.html','w') as file:
    file.write('%s' % final)