# -*- coding: utf-8 -*-
"""
Downloading MLP:FiM episodes summaries

@author: Polonius
"""

import episodesList as ep
import requests, json
import re
import os

def getArticleID(title):
    endpoint = "https://mlp.fandom.com/api/v1/Search/List?query="+title+"&limit=200"
    articlesOut=json.loads(requests.get(endpoint).text)
    articles=articlesOut['items']
    idT=0
    for article in articles:
        if article['title']==title:
            idT=article['id']
            break
    return idT

def clearText(text):
    out=text.replace('\xf1','n')
    out=out.replace('\xea','e')
    out=out.replace('\xe0','a')
    out=out.replace('\xe8','e')
    out=out.replace('\xa1','!')
    out=out.replace('\xa0',' ')
    out=out.replace('\u2019',"'")
    out=out.replace('\u0153',"oe")
    return out

def importSummaries():
    #Get episodes titles
    titles=ep.getTitles('episodesList.txt')
    
    # Create directory
    try:
        # Create target Directory
        os.mkdir('episodes')
        print("Directory Created") 
    except FileExistsError:
        print("Directory already exists")
    
    for title in titles:    
        idT=getArticleID(title)
        if not idT:
            continue
        endpoint = "https://mlp.fandom.com/api/v1/Articles/AsSimpleJson?id="+str(idT)
        articlesOut=json.loads(requests.get(endpoint).text)
        
        text=[title+'\n\n']
        isSummary=False
        for section in articlesOut['sections']:
            if section['title']=='Summary':
                isSummary=True
            elif isSummary and (re.search('See also',section['title']) or\
                                re.search('References',section['title']) or\
                                re.search('Quotes',section['title'])):
                isSummary=False
            elif isSummary:
                content=section['content']
                for paragraph in content:
                    try:
                        text.append(clearText(paragraph['text']+'\n\n'))
                    except:
                        continue
                    
            final=''.join(text)
            
        #Some characters can't be used in the file name
        title=title.replace('?','')
        title=title.replace('!','')
        title=title.replace('"','')
        title=title.replace(':','-')
        with open('episodes/'+re.sub(' ','_',title)+'.txt','w') as file:
            file.write('%s' % final)
            
    print('Summaries of episodes succesful imported')