import os
import gkeepapi
from configparser import SafeConfigParser


class myNote:
    text = ""
    tags = set()
    date = ""

    def __init__(self, text, tags, date):
        self.text = text
        self.tags = tags
        self.date = date

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
        noteDate = note.timestamps.created
        noteTags = set()
        for word in noteText.lower().split():
            if "#" in word:
                word = cleanText(word)
                if word not in noteTags:
                    noteTags.update([word])
        
        parsedNote = myNote(noteText, noteTags, noteDate)
        returnNotes.append(parsedNote)

    return returnNotes

def tagsRanking():
    gnotes = getNotes()
    tags = {}
    textToReturn = ""
    repetitions = 1

    for nota in gnotes:
        for word in nota.tags:
            if word not in tags:
                tags[word] = 1
            else:
                tags[word] += 1
    
    sorted_d = sorted(tags.items(), key=lambda x: x[1])
    
    
    for element in sorted_d:
        if element[1] > repetitions:
            textToReturn += element[0] + ": " + str(element[1]) + "\n"

    return textToReturn

def printByTag(tag):
    gnotes = getNotes()
    tag = cleanText(tag)
    cont = 1
    textToReturn = ""

    for note in gnotes:
        if tag in note.tags:
            textToReturn += "(" + str(note.date.strftime("%d-%B-%Y")) + ") Text in note " + str(cont) + ": \n"
            textToReturn += note.text + "\n"
            textToReturn += "------------------------------------------------------------------\n"
            cont += 1

    if textToReturn == "":
        textToReturn = "No dreams found with that tag"
        
    return textToReturn
