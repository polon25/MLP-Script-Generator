# -*- coding: utf-8 -*-
"""
MLP:FiM Scripts generator based on n-grams

@author: Polonius
"""

import episodesList as ep
from collections import defaultdict
import random
import re
import os

def generateScript():
    #Get episodes titles
    titles=ep.getTitles('episodesList.txt')
    
    #Merge all scripts into one for easier work
    script=''
    for title in titles:
        title=title.replace('?','')
        title=title.replace('!','')
        title=title.replace('"','')
        title=title.replace(':','-')
        fileName='scripts/'+re.sub(' ','_',title)+'.html'
        with open(fileName,'r') as file:
            for line in file:
                script=script+line
    
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
        if re.search("<dl><dd><b>",prev):
            starts.append((prev,current))
        #Create transition method
        trigramTransitions[(prev,current)].append(nextt)
    
    #Choose starting words
    prev,current=random.choice(starts)
    result=[prev,current]
    
    #Various counters for text formatting
    prolog=True
    prologI=0
    
    dlCounter=1 #<dl> and </dl>
    dlCounterSteps=0
    itCounter=0 #<i> and </i>
    itCounterSteps=0
    bCounter=1 #<b> and </b>
    bCounterSteps=1
    
    #Generate script
    while True:
        nextWords=trigramTransitions[(prev,current)]
        nextt=random.choice(nextWords)
        
        prev,current=current,nextt
        result.append(current)
        
        #Adding the theme song
        if prolog:
            prologI=prologI+1
            if prologI>100 and re.search('</dl>', current):
                prolog=False
                result.append('<dl><dd>'+\
                '[<a class="mw-redirect" href="/wiki/Theme_song"'+\
                'title="Theme song">theme song</a>]</dd></dl>')
        
        #Keep in place formatting
        if re.search('<dl>',current):
            dlCounter=dlCounter+1
        if re.search('</dl>',current):
            dlCounter=dlCounter-1
        if dlCounter>1:
            dlCounterSteps=dlCounterSteps+1
        if dlCounterSteps>150:
            result.append('</dl>\n')
            dlCounter=dlCounter-1
            dlCounterSteps=0
        if dlCounter>2:
            for i in range(dlCounter):
                result.append('</dl>\n')
            dlCounter=0
        elif dlCounter<0:
            dlCounter=0
            
        if re.search('<i>',current):
            itCounter=itCounter+1
        if re.search('</i>',current):
            itCounter=itCounter-1
            itCounterSteps=0
        if itCounter>1:
            for i in range(itCounter):
                result.append('</i>')
            itCounter=0
            itCounterSteps=0
        elif itCounterSteps>2:
            result.append('</i>')
            itCounter=itCounter-1
            itCounterSteps=0
        elif itCounter>0:
            itCounterSteps=itCounterSteps+1
        elif itCounter<0:
            itCounter=0
            
        if re.search('<b>',current):
            bCounter=bCounter+1
        if re.search('</b>',current):
            bCounter=bCounter-1
            bCounterSteps=0
        if bCounter>1:
            for i in range(bCounter):
                result.append('</b>')
            bCounter=0
            bCounterSteps=0
        elif bCounterSteps>2:
            result.append('</b>')
            bCounter=bCounter-1
            bCounterSteps=0
        elif bCounter>0:
            bCounterSteps=bCounterSteps+1
        elif bCounter<0:
            bCounter=0
            
        
        #The end of the script
        if prev=='</dd><dd>[credits]':
            #Shrink the script, so it'll have a show-lenght
            resultTmp=result[:1100]
            resultTmp.append('</b></i>')
            resultTmp=resultTmp+result[-1100:]
            result=resultTmp
            final=" ".join(result)
            final=final.replace('</dd>','</dd>\n')
            break
    
    try:
        # Create target Directory
        os.mkdir('newScripts')
        print("Directory Created") 
    except FileExistsError:
        print("Directory already exists")
    
    #Write script to the file
    with open('newScripts/newScript.html','w') as file:
        file.write('%s' % final)
        
    print('New transcript created')