# -*- coding: utf-8 -*-
"""
Downloading MLP:FiM scripts

@author: Polonius
"""

import episodesList as ep
import re
from bs4 import BeautifulSoup
import requests

#Get rid of some strange characters
def clearText(text):
    out=text.replace('\xf1','n')
    out=out.replace('\xea','e')
    out=out.replace('\xe0','a')
    out=out.replace('\xe8','e')
    out=out.replace('\xa1','!')
    out=out.replace('\u2019',"'")
    return out

#Get list of titles
#ep.importTitles()
titles=ep.getTitles('episodesList.txt')

#Download scripts of each episode
for title in titles:
    url='https://mlp.fandom.com/wiki/Transcripts/'+re.sub(' ','_',title)
    soup=BeautifulSoup(requests.get(url).text,'html5lib')
    scenes=soup('dl')
    #Some characters can't be used in the file name
    title=title.replace('?','')
    title=title.replace(':','-')
    #Write .html file with script
    with open('scripts/'+re.sub(' ','_',title)+'.html','w') as file:
        file.write('<dl><dd><b>%s</b></dd></dl>\n' % title)
        for scene in scenes:
            scene=str(scene)
            scene=clearText(scene) #Get rid of some strange characters
            file.write('%s\n' % scene)