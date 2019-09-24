import os
import gkeepapi
from configparser import SafeConfigParser


class myNote:
    text = ""
    tags = set()

    def __init__(self, text, tags):
        self.text = text
        self.tags = tags

def cleanText(text):
    text = text.lower()
    text = text.replace(".","")
    text = text.replace(",","")
    text = text.replace(":","")
    text = text.replace("\"","")
    text = text.replace("!","")
    text = text.replace("á","a")
    text = text.replace("é","e")
    text = text.replace("í","i")
    text = text.replace("ó","o")
    text = text.replace("ú","u")
    text = text.replace("*","")
    text = text.replace("#","")

    return text

def readConfig():
    # Read environ variables
    user = str(os.environ["user"])
    password = str(os.environ["password"])

    return user, password

def getNotes():
    user, password = readConfig()
    keep = gkeepapi.Keep()
    success = keep.login(user, password)
    returnNotes = []
    
    # Find by labels
    gnotes = keep.find(labels=[keep.findLabel('Sueño')])

    for note in gnotes:
        noteText = note.text
        noteTags = set()
        for word in noteText.lower().split():
            if "#" in word:
                word = cleanText(word)
                if word not in noteTags:
                    noteTags.update([word])
        
        parsedNote = myNote(noteText, noteTags)
        returnNotes.append(parsedNote)

    return returnNotes

def tagsRaking(gnotes):
    gnotes = getNotes()
    tags = {}
    textToReturn = ""

    for nota in gnotes:
        for word in nota.tags:
            if word not in tags:
                tags[word] = 1
            else:
                tags[word] += 1
    
    sorted_d = sorted(tags.items(), key=lambda x: x[1])
    
    for element in sorted_d:
        if element[1] > 1:
            textToReturn += element[0] + ": " + str(element[1]) + "\n"

    return textToReturn

def printByTag(tag):
    gnotes = getNotes()
    tag = cleanText(tag)
    cont = 1
    textToReturn = ""

    for note in gnotes:
        if tag in note.tags:
            textToReturn += "Text in note " + str(cont) + ": " + "\n"
            textToReturn += note.text + "\n"
            textToReturn += "------------------------------------------------------------------\n"
            cont += 1

    return textToReturn