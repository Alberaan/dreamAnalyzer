import os
import gkeepapi
from configparser import SafeConfigParser


class myNote:
    text = ""
    tags = set()
    date = ""
    id = ""

    def __init__(self, id, text, tags, date):
        self.text = text
        self.id = id
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
        noteId = note.id
        noteText = note.text
        noteDate = note.timestamps.created
        noteTags = set()
        for word in noteText.lower().split():
            if "#" in word:
                word = cleanText(word)
                if word not in noteTags:
                    noteTags.update([word])
        
        parsedNote = myNote(noteId, noteText, noteTags, noteDate)
        returnNotes.append(parsedNote)

    return returnNotes

def tagsRanking(text):
    repetitions = 1
    if len(text.split(" ")) > 2:
        return "Available commands:\nRanking: prints occurrences of repeated dream tags\nSearch [tag]: searches all dreams with the provided tag"
    if len(text.split(" ")) == 2:
        if text.split(" ")[1].isdigit():
            repetitions = int(text.split(" ")[1])
        
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
        if element[1] >= repetitions:
            textToReturn += element[0] + ": " + str(element[1]) + "\n"

    return textToReturn

def printById(text):
    if len(text.split(" ")) != 2:
        return "Please provide Read + ID"
    id = text.split(" ")[1]
    gnotes = getNotes()
    textToReturn = ""
    
    for note in gnotes:
        if note.id == id:
            textToReturn += "(" + str(note.date.strftime("%d-%m-%Y")) + ")\n"
            textToReturn += note.text + "\n"
            textToReturn += "[ID: " + note.id + "]\n"
            textToReturn += "------------------------------------------------------------------\n"
            return textToReturn
       return "Note not found"
            
def printByTag(text):
    if len(text.split(" ")) <= 1:
        return "Please provide at least one tag"
    
    textCleaned = cleanText(text)
    tags = textCleaned.split(" ")[1:]
    gnotes = getNotes()
    cont = 1
    textToReturn = ""

    for note in gnotes:
        returnThisNote = True
        for tag in tags:
            if tag not in note.tags:
                returnThisNote = False
        if returnThisNote == True:
            textToReturn += "(" + str(note.date.strftime("%d-%m-%Y")) + ") Note " + str(cont) + ": \n"
            textToReturn += note.text + "\n"
            textToReturn += "[ID: " + note.id + "]\n"
            textToReturn += "------------------------------------------------------------------\n"
            cont += 1

    if textToReturn == "":
        textToReturn = "No dreams found with that tag"
        
    return textToReturn
