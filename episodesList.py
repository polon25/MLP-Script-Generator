# -*- coding: utf-8 -*-
"""
Downloading list of MLP:FiM episodes from wikia (at least some of them)

@author: Polonius
"""

import requests, json
import re

#Create a .txt file with episodes titles
def importTitles():
    # Get list of all transcript pages
    endpoint = "https://mlp.fandom.com/api/v1/Search/List?query=transcript&limit=300"
    articlesOut=json.loads(requests.get(endpoint).text)
    
    titles=[]
    for article in articlesOut['items']:
        title=re.split("Transcripts/",article['title'])[1]
        if not (re.search("Equestria Girls",title) or re.search("The Movie",title)
            or re.search("shorts",title) or re.search("Part 2",title)):
            titles.append((article['id'],title))
            #Because there're problems with getting 'part 2' websites
            if re.search("Part 1",title) or re.search("part 1",title):
                titles.append((article['id']+1,re.sub('1','2',title)))
           
    #It's not the most accurate sorting btw
    titles.sort()
    
    with open('episodesList.txt','w') as file:
        for idT, title in titles:
            file.write('%s\n' % title)
            
    print('List of episodes succesful imported')

#Get titles list       
def getTitles(fileName):
    titles=[]
    with open(fileName,'r') as file:
        for title in file:
            titles.append(re.sub('\n','',title))        
    return titles