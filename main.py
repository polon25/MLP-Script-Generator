# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
MLP:FiM episode's plot generator based on n-grams
GUI

@author: Polonius
"""

import tkinter as tk
from tkinter import messagebox as msb

import episodesList as epList
import scriptsMLP as scripts
import generateScript as genScript
import episodesMLP as episodes
import generatePlot as genEpisode

class MainWindow:    
    def __init__(self):
        self.window=tk.Tk()
        self.window.title("MLP:FiM Episode Generator")
        self.window.geometry("320x250")
        self.createButtons()
        self.window.mainloop()
        
    def createButtons(self):
        tk.Label(self.window).pack()
        #Add a book button
        addBook=tk.Button()
        addBook["text"]="Import list of episodes"
        addBook["command"]=self.importTitles
        addBook.pack()
        #Print all books button
        addBook=tk.Button()
        addBook["text"]="Import transcripts"
        addBook["command"]=self.importScripts
        addBook.pack()
        #Search button
        addBook=tk.Button()
        addBook["text"]="Import summaries"
        addBook["command"]=self.importSummaries
        addBook.pack()
        #Search button
        addBook=tk.Button()
        addBook["text"]="Generate transcript"
        addBook["command"]=self.generateScript
        addBook.pack()
        #Search button
        addBook=tk.Button()
        addBook["text"]="Generate episode"
        addBook["command"]=self.generateEp
        addBook.pack()
        #Exit button
        exit=tk.Button()
        exit["text"]="Exit"
        exit["command"]=self.quit
        exit.pack()
        
        label=tk.Label(text="MLP:FiM Episode Generator\nby Polonius\n2020")
        label.pack()
    
    def importTitles(self):
        epList.importTitles()
        msb.showinfo("Yay", "Episodes list has been imported") 
    def importScripts(self):
        scripts.importScripts()
        msb.showinfo("Yay", "Episodes transcripts have been imported\ninto the 'scripts' folder") 
    def importSummaries(self):
        episodes.importSummaries()
        msb.showinfo("Yay", "Episodes summaries have been imported\ninto the 'episodes' folder") 
    def generateScript(self):
        genScript.generateScript()
        msb.showinfo("Yay", "Episode transcript has been generated\nin the 'newScripts' folder")    
    def generateEp(self):
        genEpisode.generateEpisode()
        msb.showinfo("Yay", "Episode has been generated\nin the 'newEpisodes' folder")
    def quit(self):
        self.window.destroy()
        
#Main program
print("MLP:FiM Episode Generator\nby Polonius\n")

mainWindow=MainWindow()

print("MLP:FiM Episode Generator has been stoped!")