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

def printHelp():
    textToReturn = "Available commands:\n"
    textToReturn += "Ranking [min]: prints occurrences of repeated dream tags. If min is provided, only prints notes tags with min number of occurrences\n"
    textToReturn += "Filter [list of tags]: searches all dreams that have the provided tags\n"
    textToReturn += "Read [ID]: prints the note with the provided ID\n"
    textToReturn += "Date [year] [month] [day]: lists dreams in that year, year+month, year+month+day\n"
    return textToReturn    
    
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
        return printHelp()
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
        return printHelp()
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
    return "No dreams where found with that ID"
            
def notesByDate(text):
    if len(text.split(" ")) > 4:
        return printHelp()
    for parameter in text.split(" ")[1:]:
        if parameter.isdigit() != True:
            return printHelp()
    
    gnotes = getNotes()
    numberOfParameters = len(text.split(" ")[1:])
    notesToReturn = []
    yearsToReturn = []
    monthsToReturn = []
    daysToReturn = []
    
    for note in gnotes:
        toReturn = True
        if numberOfParameters == 0:
            if note.date.year not in yearsToReturn:
                uearsToReturn.append(note.date.year)
        if numberOfParameters >= 1:
            if note.date.year != int(text.split(" ")[1]):
                if note.date.month not in monthsToReturn:
                    monthsToReturn.append(note.date.month)
                toReturn = False
        if numberOfParameters >= 2:
            if note.date.month != int(text.split(" ")[2]):
                if note.date.day not in daysToReturn:
                    daysToReturn.append(note.date.day)
                toReturn = False
        if numberOfParameters == 3:
            if note.date.day != int(text.split(" ")[3]):
                toReturn = False
        if toReturn == True:
            notesToReturn.append(note.id)
        
        toReturn = True
        
    textToReturn = "Number of notes in that period: " + str(len(notesToReturn)) + "\n"
    for line in notesToReturn:
        textToReturn += "<id>"+ line + "</id>\n"
    
    if numberOfParameters == 0:
        for year in yearsToReturn:
            textToReturn += "<year>" + str(year) + "</year>\n"
    
    if numberOfParameters == 1:
        for month in monthsToReturn:
            textToReturn += "<month>" + str(month) + "</month>\n"
    
    if numberOfParameters == 2:
        for day in daysToReturn:
            textToReturn += "<day>" + str(day) + "</day>\n"
            
    if textToReturn == "":
        return "No dreams found on that date"
    return textToReturn
    
def printByTag(text):
    if len(text.split(" ")) <= 1:
        return printHelp()
    
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
