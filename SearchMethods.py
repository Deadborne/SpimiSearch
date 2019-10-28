from pathlib import Path
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
import SPIMISearchEngine

blockPath = Path("C:/Users/Sean/workspace/COMP 479 Information Retrieval/blocks")
tokenizer = RegexpTokenizer(r'\w+') #allows tokenization without punctuation

def singleQuery(caseFold, noNumbers, oneFiftyStopWords):
    
    finalDict = SPIMISearchEngine.readObject("finaldictionary.bin")
    query = input ("Enter a single word query: ")
    
    #If we used lossy compression techniques on the dictionary, we should do so on the query too.
    if (caseFold): query = (query.lower())
    if (noNumbers): query = (re.sub(r'\d+', '', query))
    tokens = tokenizer.tokenize(query) #splits the query into tokens
    if (oneFiftyStopWords):
        stopWords = set(stopwords.words('english'))
        tokens = [w for w in tokens if not w in stopWords]    
    
    if (len(tokens) == 0):
        print ("Your query contained only stopwords or numbers even after you specifically chose to remove them from your dictionary.")
        print ("Please choose a query with those choices in mind.")
        return
    
    if (len(tokens) > 1):
        print ("Hey, smart aleck. That was more than one word, wasn't it?")
        print ("You probably should have picked a different option!")
        return       
    
    listToReturn = (finalDict.get(tokens[0])) #DocID list for first term in query. 
    print (query + " " + str(listToReturn))      

def andQuery(caseFold, noNumbers, oneFiftyStopWords):
    
    finalDict = SPIMISearchEngine.readObject("finaldictionary.bin")
    query = input ("Enter your AND query, with every word separated by spaces: ")
    
    #If we used lossy compression techniques on the dictionary, we should do so on the query too.
    if (caseFold): query = (query.lower())
    if (noNumbers): query = (re.sub(r'\d+', '', query))
    tokens = tokenizer.tokenize(query) #splits the query into tokens
    if (oneFiftyStopWords):
        stopWords = set(stopwords.words('english'))
        tokens = [w for w in tokens if not w in stopWords]
        
    if (len(tokens) == 0):
        print ("Your query contained only stopwords or numbers even after you specifically chose to remove them from your dictionary.")
        print ("Please choose a query with those choices in mind.")
        return    
    
    listToReturn = (finalDict.get(tokens[0])) #DocID list for first term in query.
    if (listToReturn == None): 
        print (query + ": []")
        return
    #If our query had only one term after compression, we just return the list.
    if (len(tokens) == 0):
        print (query + " " + str(listToReturn))        
    #if not, we subtract docIDs from it until we have the intersection of the docID's for all terms
    else:
        for x in range (1, len(tokens)):
            intersectList = finalDict.get(tokens[x])
            if intersectList == None: intersectList = []
            listToReturn = [value for value in listToReturn if value in intersectList]
        print(query + ": " + str(listToReturn))
        
def orQuery(caseFold, noNumbers, oneFiftyStopWords):
    
    finalDict = SPIMISearchEngine.readObject("finaldictionary.bin")
    query = input ("Enter your OR query, with every word separated by spaces: ")
    
    #If we used lossy compression techniques on the dictionary, we should do so on the query too.
    if (caseFold): query = (query.lower())
    if (noNumbers): query = (re.sub(r'\d+', '', query))
    tokens = tokenizer.tokenize(query) #splits the query into tokens
    if (oneFiftyStopWords):
        stopWords = set(stopwords.words('english'))
        tokens = [w for w in tokens if not w in stopWords]    
    
    if (len(tokens) == 0):
        print ("Your query contained only stopwords or numbers even after you specifically chose to remove them from your dictionary.")
        print ("Please choose a query with those choices in mind.")
        return
        
    listToReturn = (finalDict.get(tokens[0])) #DocID list for first term in query.
     
    if (listToReturn == None): 
        listToReturn = []
     
    #If our query had only one term after compression, we just return the list.
    if (len(tokens) == 1):
        print (query + ": " + str(listToReturn))        
    #if not, we create the union of docID lists
    else:
        for i in range (1, len(tokens)): 
            addToList = finalDict.get(tokens[i])
            if (addToList == None): addToList = []
            listToReturn = listToReturn + addToList
        listToReturn = sorted(listToReturn, key = Counter(listToReturn).get, reverse = True) #sorts by number of occurrences
        listToReturn = list(dict.fromkeys(listToReturn)) #removes duplicates
        print(query + ": " + str(listToReturn))      
        
     
     
    #main method   
if __name__ == '__main__':
    
        print("      ___           ___           ___           ___           ___           ___           ___       ___     ")
        print("     /\  \         /\__\         /\__\         /\  \         /\  \         /\  \         /\__\     /\  \    ")
        print("    /::\  \       /:/  /        /::|  |       /::\  \       /::\  \       /::\  \       /:/  /    /::\  \   ")
        print("   /:/\ \  \     /:/__/        /:|:|  |      /:/\:\  \     /:/\:\  \     /:/\:\  \     /:/  /    /:/\:\  \  ")
        print("  _\:\~\ \  \   /::\  \ ___   /:/|:|  |__   /:/  \:\  \   /:/  \:\  \   /:/  \:\  \   /:/  /    /::\~\:\  \ ")
        print(" /\ \:\ \ \__\ /:/\:\  /\__\ /:/ |:| /\__\ /:/__/ \:\__\ /:/__/ \:\__\ /:/__/_\:\__\ /:/__/    /:/\:\ \:\__\ ")
        print(" \:\ \:\ \/__/ \/__\:\/:/  / \/__|:|/:/  / \:\  \ /:/  / \:\  \ /:/  / \:\  /\ \/__/ \:\  \    \:\~\:\ \/__/")
        print("  \:\ \:\__\        \::/  /      |:/:/  /   \:\  /:/  /   \:\  /:/  /   \:\ \:\__\    \:\  \    \:\ \:\__\  ")
        print("   \:\/:/  /        /:/  /       |::/  /     \:\/:/  /     \:\/:/  /     \:\/:/  /     \:\  \    \:\ \/__/  ")
        print("    \::/  /        /:/  /        /:/  /       \::/  /       \::/  /       \::/  /       \:\__\    \:\__\    ")
        print("     \/__/         \/__/         \/__/         \/__/         \/__/         \/__/         \/__/     \/__/    \n")
        print("\n                        ----Disclaimer: Exact matches only!----\n")
        
        caseFold = False
        noNumbers = False
        thirtyStopWords = False
        oneFiftyStopWords = False
        
        choice = input("Do you wish to use casefolding? y/n\n")
        if (choice.lower() == ("y" or "yes")): caseFold = True
        choice = input("Do you wish to remove numbers? y/n\n")
        if (choice.lower() == ("y" or "yes")): noNumbers = True
        choice = input("Do you wish to remove stopwords?\n")
        if (choice == ("y" or "yes")): oneFiftyStopWords = True
        
        while (1):
            choice = input ("\nType of search: \n1: Single word\n2: Multiple words (And query) \n3: Multiple words (Or query)\n4: All done\n")
            if (choice == "1"): singleQuery(caseFold, noNumbers, thirtyStopWords, oneFiftyStopWords)
            if (choice == "2"): andQuery(caseFold, noNumbers, thirtyStopWords, oneFiftyStopWords)
            if (choice == "3"): orQuery(caseFold, noNumbers, thirtyStopWords, oneFiftyStopWords)
            if (choice == "4"): 
                print ("Goodbye!")
                break
    