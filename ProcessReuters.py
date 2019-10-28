from pathlib import Path

writePath = Path("C:/Users/Sean/workspace/COMP 479 Information Retrieval/articles")
readPath = Path("C:/Users/Sean/workspace/COMP 479 Information Retrieval/reuters")
def processFiles():
    idTracker = 1
    #First, we split every reuter sgm into articles.
    for x in range (22):
       
        fileName = ""
        newID = ""
        title = ""
        body = ""
    
        #make sure we read the filename correctly
        if (x<10):
            fileName = ('reut2-00' + str(x) + ('.sgm'))
        else:
            fileName = ('reut2-0' + str(x) + ('.sgm'))
        with open (readPath / fileName) as f:
            #We find the NewID. We can make this the title of a .txt file, or the documentID
            content = f.read() #the whole content of the file as a string
            docIDfind = content.split("NEWID=\"") #our file is now split into lists starting with newID
            docIDfind.pop(0)
            for y in range (0, len(docIDfind)):
                #knowing how big the newID is, so that we can grab it
                offsetter = 0
                if (int(idTracker/10) < 1):
                    offsetter = 1
                elif (int(idTracker/10) > 0 and int(idTracker/10) < 10 ):
                    offsetter = 2
                elif (int(idTracker/10) > 9 and int(idTracker/10) < 100 ):
                    offsetter = 3
                elif (int(idTracker/10) > 99 and int(idTracker/10) < 1000 ):
                    offsetter = 4
                elif (int(idTracker/10) > 999 and int(idTracker/10) < 10000 ):
                    offsetter = 5
                elif (int(idTracker/10) > 9999 and int(idTracker/10) < 100000 ):
                    offsetter = 6
                newID = (docIDfind[y][0:offsetter]) #Grab the newID!
                idTracker+=1
                writer = open(writePath / (newID+".txt"),"w+") #write path, to use later
                #now we grab the Title
                if (docIDfind[y].find('<TITLE>') != -1):
                    titleFind = docIDfind[y].split("<TITLE>")
                    titleFind.pop(0)
                    titleLimit = (titleFind[0].index('</TITLE>')) #finding the index of the delimiter
                    title = (titleFind[0][0:titleLimit]) #Grab the Title!
                    #now we grab the body
                    if((titleFind[0].find('<BODY>')) != -1):
                        bodyFind = titleFind[0].split("<BODY>")
                        bodyFind.pop(0)
                        bodyLimit = (bodyFind[0].index('</BODY>'))
                        body = (bodyFind[0][0:bodyLimit]) #Grabbed the body!
                    else: #If we can't find a body, we make the body blank
                        body = ""
                    writer.write(title+"\n "+body ) #create article file
                else: #If there is no title, there is no body (a fact of the reuters corpus)
                    title ="" 
                    body = ""  
                print("Article #" + str(newID)+" has been processed.")
        f.close()    
        writer.close()
    print (":::Preprocessing complete!:::")

if __name__ == '__main__':
    processFiles() 