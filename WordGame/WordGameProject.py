
# coding: utf-8

# In[ ]:


import random
from datetime import datetime
from operator import itemgetter

#list of all words
words = []
#list of big words
bigWords = []
#list of small words
smallWords = []
wordsOriginal = open('words.txt')

# puts words.txt in list words
with wordsOriginal as inputfile:
    for line in inputfile:
        addWord = line.split()
        words.append(addWord.pop())

# seperates list into two lists of big words and small words
for word in words:
    if len(word) >= 7:
        bigWords.append(word)
    else:
        smallWords.append(word)

# output random word from big words
randomBigWord = random.choice(bigWords)
print(randomBigWord)
print()

#start timer
startTime = datetime.now()

# all words input
wordInput = []
wordInput.append(input("Word 1: "))
wordInput.append(input("Word 2: "))
wordInput.append(input("Word 3: "))
wordInput.append(input("Word 4: "))
wordInput.append(input("Word 5: "))
wordInput.append(input("Word 6: "))
wordInput.append(input("Word 7: "))

#end timer
endTime = datetime.now()
#total time
totalTime = (endTime - startTime).total_seconds()
totalTime = str(round(totalTime, 2))
print()

def manageHighscores():
    kList = []
    vList = []
    vStrList = []
    highscore = open("TopScorersList2","r+")

    # for each line in the file strip it and split it
    # change the value to a number for sorting
    # add back to a dictionary and sort them by the value

    for line in highscore:
        line = line.strip()
        lineList = line.split(",")
        key,value = lineList
        value = float(value)
        kList.append(key)
        vList.append(value)
    doubleList = [list(x) for x in zip(*sorted(zip(vList, kList), key=itemgetter(0)))]
    kList = doubleList[1]
    vList = doubleList[0]
    highscore.close()

    # now put them into to seperate lists
    # change the value back to a string
    kList = list(kList)

    for v in vList:
        vStrList.append(str(v))
    #vStrList = list(vStrList)
    #the lists are only 10 wide because we only need to remember 10 highscores
    #del kList[10:]
    #del vStrList[10:]

    finalOutputList = []
    listOutputNum = 0
    tempList = list(vStrList)

    vStrList = []
    for sublist in tempList:
            sublist = str(sublist)
            vStrList.append(sublist)

    open("TopScorersList2", 'w').close()

    highscore = open("TopScorersList2","r+")

    # make a string of first index of the two lists
    #add that string to a final list
    #write that list line by line to the file
    while listOutputNum < len(kList):
        inputStringK = str(kList[listOutputNum])
        inputStringV = str(vStrList[listOutputNum])
        inputString = inputStringK + "," + inputStringV + "\n"
        finalOutputList.append(inputString)
        highscore.write(finalOutputList[listOutputNum])
        listOutputNum+=1
    #does not seem to work without closing and reopening file
    highscore.close()
    highscore = open("TopScorersList2","r+")
    print("HIGHSCORE")
    tenPrints = 0
    for line in highscore:
        if tenPrints < 10:
            line = line.strip()
            lineList = line.split(",")
            key,value = lineList
            print("Name:",key,"Time:",value,"seconds")
            print()
            tenPrints+=1
    highscore.close()


def checkValidity(checkWords,randomBigWordIn,totalTimeIn):
    randomBigWord = randomBigWordIn
    totalTime = totalTimeIn
    allValid = True
    duplicates = set()
    for word in checkWords:
        #first validity check is the word at least 3 letters
        if word == "":
            allValid = False
            tempWordRemove = checkWords.index(word)
            print("*EMPTY*", "is not a valid word it is empty")
            checkWords[tempWordRemove] = -1 #to symbolise empty

        #second validity check is the word at least 3 letters
        elif len(word) < 3:
            allValid = False
            tempWordRemove = checkWords.index(word)
            print(word, "is not a valid word it has less than three letters")
            checkWords[tempWordRemove] = -1

        else:
            #third test check if all of the letters are in the word
            #makes sure checking is done in the same case
            letterInWord = list(word.lower())
            bigWordLetters = list(randomBigWord.lower())

            # for every letter in the word check if that letter is in the random word if it is remove it
            letterInWordSuccessful = True
            for letter in letterInWord:
                if letter not in bigWordLetters:
                    letterInWordSuccessful = False
                    allValid = False
                    tempWordRemove = checkWords.index(word)
                    print(word, "is not a valid word it uses characters not in the word")
                    checkWords[tempWordRemove] = -1
                    break
                else:
                    if(letterInWord.count(letter) > bigWordLetters.count(letter)):
                        letterInWordSuccessful = False
                        allValid = False
                        tempWordRemove = checkWords.index(word)
                        print(word, "is not a valid word it uses a letter more times than it appears in the word")
                        checkWords[tempWordRemove] = -1
                        break
                    else:
                        letterInWordSuccessful = True


            #fourth test is the word in the dictionary
            if letterInWordSuccessful == True:
                if word not in words:
                    allValid = False
                    tempWordRemove = checkWords.index(word)
                    print(word, "is not a valid word it is not in the dictionary")
                    checkWords[tempWordRemove] = -1
                else:
                    #fifth test checking for duplicates

                    if word not in duplicates:
                        duplicates.add(word)

                        #sixth check if the word is the same as the source word
                        if word == randomBigWord:
                            allValid = False
                            tempWordRemove = checkWords.index(word)
                            print(word, "is not a valid word it is the same as the source word")
                            checkWords[tempWordRemove] = -1
                        else:
                            print(word, "is a valid word")

                    else:
                        allValid = False
                        tempWordRemove = checkWords.index(word)
                        print(word, "is not a valid word it is a duplicate")
                        checkWords[tempWordRemove] = -1

    #print time if all words were valid
    if allValid == True:
        print()
        printingTime(totalTime, "Seconds")
        print()
        userName = input("Congrats, what is your name? ")
        print()
        highscore = open("TopScorersList2","a")
        inputString = userName + "," + totalTime
        #write our result to the highscore table
        highscore.write(inputString)
        #close and reopen because doesnt work otherwise
        highscore.close()
        manageHighscores()
        highscore = open("TopScorersList2", "r")
        playerPosition = 1
        fullLength = 0
        stopIncrementing = False

        for line in highscore:
            line = line.strip()
            if inputString == line:
                stopIncrementing = True
            if stopIncrementing == False:
                playerPosition +=1
            fullLength+=1
        print("Your position is",playerPosition,"out of",fullLength)
        highscore.close()
    else:
        print()
        printingTime("Invalid","Time")

    restart()

#output time if words are valid
def printingTime(timeToPrint, message):
    print(timeToPrint, message)
def restart():
    restart = input("Do you want to play again y/n?")
    restart = restart.lower()
    if restart == "y":
        print()
        # output random word from big words
        randomBigWord = random.choice(bigWords)
        print(randomBigWord)
        print()

        #start timer
        startTime = datetime.now()

        # all words input
        wordInput = []
        del wordInput[:]

        wordInput.append(input("Word 1: "))
        wordInput.append(input("Word 2: "))
        wordInput.append(input("Word 3: "))
        wordInput.append(input("Word 4: "))
        wordInput.append(input("Word 5: "))
        wordInput.append(input("Word 6: "))
        wordInput.append(input("Word 7: "))

        #end timer
        endTime = datetime.now()
        #toal time
        totalTime = (endTime - startTime).total_seconds()
        totalTime = str(round(totalTime, 2))
        print()

        checkValidity(wordInput,randomBigWord,totalTime)


    else:
        print()
        print("Goodbye")

checkValidity(wordInput,randomBigWord,totalTime)
