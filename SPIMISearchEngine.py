from pathlib import Path
import token
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from pickle import HIGHEST_PROTOCOL,dump,load

#Path where you want to dump all 21578 Reuters text files can be specified here
writePath = Path("C:/Users/Sean/workspace/COMP 479 Information Retrieval/articles")
blockPath = Path("C:/Users/Sean/workspace/COMP 479 Information Retrieval/blocks")
blockNumber = 1 #determines which block to write to
fileNumber = 1 #determines which file to write to
tokenizer = RegexpTokenizer(r'\w+') #allows tokenization without punctuation
docIDcheck = 1

#Methods required for SPIMI    
def addToDictionary(dictionary, term):
    dictionary[term] = []
    return dictionary[term]

def getPostingsList(dictionary, term):
    return dictionary[term]

def addToPostings(postingsList, docID):
    if docID not in postingsList:
        postingsList.insert(len(postingsList), docID)
    else:
        postingsList
    return postingsList #not sure if needed        
def writeBlockToDisk(sortedTerms, dictionary, outputFile):
    with open (blockPath / outputFile,"w+") as f:
        #f.write (sortedTerms)
        for term in sortedTerms:
            f.write(term + " ")
            for x, y in dictionary.items():
                if (term == x):
                    f.write(str(y) + "\n")
    f.close()
        
#Serializing 
def saveObject(objToSave, fileDirectory):
    dump(objToSave,fileDirectory,HIGHEST_PROTOCOL)
def readObject(objToRead):
    with open(blockPath/objToRead,'rb') as fileDirectory: objToRead = load(fileDirectory)
    fileDirectory.close()
    return objToRead;

#SPIMI
def spimiInvert(tokenStream):
    filename = "blockT" + str(blockNumber) +".bin"
    with open(blockPath/filename,"wb") as savedTerms:
        outputFile = ("block" + str(blockNumber) + ".txt") 
        dictionary = {}
        for token in tokenStream:
            term = token[0]
            docID = token[1]
            if term not in dictionary:
                postingsList = addToDictionary (dictionary, term)
            else:
                postingsList = getPostingsList(dictionary,term)
            addToPostings(postingsList,docID)
        sortedTerms = sorted(dictionary)
        writeBlockToDisk(sortedTerms, dictionary, outputFile)
        saveObject(sortedTerms,savedTerms)
        dicFileName = "blockD" + str(blockNumber) +".bin"
        with open(blockPath/dicFileName,"wb") as savedDict:
            saveObject(dictionary,savedDict)
    return outputFile

#the main SPIMI function takes 3 boolean parameters, for if we want to apply case folding, remove numbers, or remove stopwords 
def spimi(caseFold, noNumbers, oneFiftyStopWords):
    
    ARTICLESPERBLOCK = 500 #Number of articles in one simulated memory block
    NUMBEROFBLOCKS = 44 #number of blocks to create
    tokenStream = [] #empty list
    #accessing global variables
    global blockNumber
    global docIDcheck
    
    for x in range (NUMBEROFBLOCKS):
        content = ""                    
        for y in range (ARTICLESPERBLOCK):
            try: reader = open(writePath / (str(docIDcheck) + ".txt"))
            except: reader = ""
            if (reader==""): break
            content = reader.read()
            if (caseFold): content = (content.lower())
            if (noNumbers): content = (re.sub(r'\d+', '', content))
            tokens = tokenizer.tokenize(content) #splits the article into tokens
            if (oneFiftyStopWords):
                stopWords = set(stopwords.words('english'))
                tokens = [w for w in tokens if not w in stopWords]
            for z in range(len(tokens)):
                tokenDocID = (tokens[z], docIDcheck) #creates a term,docID tuple
                tokenStream.append(tokenDocID) #creates a list of 500 articles worth of tuples
            docIDcheck += 1
            content = ""
        spimiInvert(tokenStream)
        tokenStream = []
        print ("Wrote " + str(ARTICLESPERBLOCK) + " articles to block" + str(blockNumber))
        blockNumber += 1
        
def blockMerge():
    BLOCKSTOMERGE = 44 # Because we'll want to adjust this for demo purposes
    masterList = list() # a list of sorted terms lists in each block (list of lists)
    masterDict = list() # a list of dictionaries in each block (list of dicts)

    blockWriter = open(blockPath / ('index.txt'),"w+") #to be moved
    
    for x in range (BLOCKSTOMERGE):
        l = readObject("blockT" + str(x+1) + ".bin")
        d = readObject("blockD" + str(x+1) + ".bin")
        masterList.append(l)
        masterDict.append(d)
    
    #putting the whole sorted terms together
    for x in range (1, BLOCKSTOMERGE):
        for l2 in range (len(masterList[x])):
            if (masterList[x][l2] not in masterList[0]):
                masterList[0].append(masterList[x][l2])
                    
    print ("Full dictionary compiled.")
    
    #putting all the docID's together now
    allTerms = sorted(masterList[0])
    print ("Full dictionary sorted.")
    
    #we have the dictionaries of each block, but they are scattered throughout the indices. We put them together.
    finalDictionary = {}
    for x in range (BLOCKSTOMERGE):
        for y in range (BLOCKSTOMERGE):
            if (y > x):
                for dictTermx, idsx in masterDict[x].items():
                    if (masterDict[y].get(dictTermx) != None): 
                        masterDict[x][dictTermx] += (masterDict[y].get(dictTermx))
                        masterDict[y].pop(dictTermx, None)
        finalDictionary.update(masterDict[x])
    
    #finally, we compound the last inverted document list    
    for term in allTerms:
        blockWriter.write(term + " ")
        for dictTerm, ids in finalDictionary.items():
            if (term == dictTerm):
                blockWriter.write(str(ids))
        blockWriter.write ("\n")
        
    with open(blockPath/"finaldictionary.bin","wb") as savedDict:
        saveObject(finalDictionary,savedDict)
    with open(blockPath/"finalterms.bin","wb") as savedTerms:
        saveObject(allTerms,savedTerms)
    print ("All done!")
                                
        
#main
if __name__ == '__main__':

    
    caseFold = False
    noNumbers = False
    oneFiftyStopWords = False
    
    choice = input("Do you wish to use casefolding? y/n\n")
    if (choice.lower() == ("y" or "yes")): caseFold = True
    choice = input("Do you wish to remove numbers? y/n\n")
    if (choice.lower() == ("y" or "yes")): noNumbers = True
    choice = input("Do you wish to remove stopwords?\n")
    if (choice == ("y" or "yes")): oneFiftyStopWords = True
    
    spimi(caseFold, noNumbers, oneFiftyStopWords)
    blockMerge()
