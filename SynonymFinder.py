#CITS1401 Project 2: Finding Synonyms by Association
#Written by Gregory Edmonds 21487148

import math
import time

#Create class: Profile
class Profile:
    
    def __init__(self,word):
        self.word = word
        self.associatedWords = {}

    def addNewProfile(self, addWord):
        if(str(addWord) not in self.associatedWords):
            self.associatedWords[str(addWord)] = 1
        else:
            self.associatedWords[str(addWord)] += 1
            
    def getProfileName(self):
        return self.word
     
    def getListOfWords(self):
        return self.associatedWords
    
    def __repr__(self):
        string = "\nWord: " + self.word + "\n\n" + "Profile:" + "\n"
        for key in self.associatedWords:
            string += "Associated Word: " + key + " Occurence: " + str(self.associatedWords[key]) + "\n"
        return string

#Loops through a sentence and adds each word to a profile if word not in common words file
def addAssociatedWords(sentence, profile, commonWords):
    for word in sentence.split(' '):
        if word != profile.getProfileName() and word != '' and word not in commonWords:
            profile.addNewProfile(word)
    return profile           

#Reads the common words file
def readCommonWordsFile(commonwords_file_name = None):
    common = []
    if(commonwords_file_name):
        try:
            commonFile = open(commonwords_file_name,'r')
            common = list(commonFile.read().splitlines())
            for word in common:
                    word = word.lower()
        except IOError as e:
            print("Error reading file: " + commonwords_file_name + " " + str(e) + "\n")
            print("Running without common word file: ")
    return common

#Reads the set file and returns a dictionary of sets, with error handling
def createSets(fileName):
    dictOfSets = {}
    tempWords = []
    try:
        file = open(fileName, 'r')
        words = file.readlines()
        for word in words:
            if(" " not in word.lstrip().rstrip()):
                if word == "\n":
                    if(tempWords):
                        dictOfSets[tempWords[0]] = tempWords
                        tempWords = []
                elif (word == words[len(words)-1]):
                    tempWords.append(word.strip("\n").lower())
                    dictOfSets[tempWords[0]] = tempWords
                    tempWords = []            
                else:
                    tempWords.append(word.strip("\n").lower())
            else:
                raise IOError("Error: set file has incorrect format. Check formatting of: " + fileName + " " + "\n")
    except PermissionError as e:
        raise IOError("Error reading file. Check file read permissions of: " + fileName + " " + str(e) + "\n")
    except IOError as e:
        print("Error reading set file: " + fileName + str(e))
        raise e
    except Exception as e:
        print("Error reading set file: " + fileName + str(e))
        raise IOError
    return(dictOfSets)

#Opens the text file which words are to be read from, with error handling
def openFile(text):
    sentences = []
    try:
        file = open(text, 'r')
        sentences = []
        endOfSentence = ['.','!','?']
        word = ''
        with file as data:
            tempword = ''
            for line in data:
                for word in line:
                    if(word in endOfSentence):
                        tempword = punctuationMaker(tempword.lower())
                        sentences.append(tempword)
                        tempword = ''
                    else:
                        tempword += word
            if(tempword.strip('\n') != ''):
                raise IOError("Error: Reached end of file with no end of line character")
    except PermissionError as e:
            raise IOError("Error reading file. Check file read permissions of: " + text + " " + str(e) + "\n")
    except IOError as e:
        raise IOError("Error reading file: " + text + str(e))
    except Exception as e:
        raise IOError("Error reading file: " + text + str(e))
    return sentences

#Compares two profiles using the cosine similarity equation
def compareTwoProfiles(profile1, profile2):
    listWordsProfile1 = profile1.getListOfWords()
    listWordsProfile2 = profile2.getListOfWords()
    value = 0
    pVector, qVector = 0, 0
    for word in listWordsProfile2:
        qVector += listWordsProfile2[word] * listWordsProfile2[word]
    for word in listWordsProfile1:
        if word in listWordsProfile2:
            value = value + listWordsProfile1[word] * listWordsProfile2[word]
        pVector += listWordsProfile1[word] * listWordsProfile1[word]
    if pVector != 0 and qVector != 0:
        endValue = value/math.sqrt(pVector*qVector)
    else:
        endValue = 0
    return endValue

#Reads a file with [',',"\'",'\"',':',';','[',']','(',')'] as space characters
#and [.,?,!] as fullstop
def punctuationMaker(sentence):
    #punctuation marks
    for ch in [',',"\'",'\"',':',';','[',']','(',')']:
        if ch in sentence:
            sentence = sentence.replace(ch, "")
    sentence = sentence.replace('\n', " ")
    sentence = sentence.replace('--', " ")
    return sentence

#Creates profiles and adds associated words to each profile
def getAllProfiles(sentences, profileSets,commonWords):
    profileDict = {}
    wordsFoundInCurrentSentence = []
    uniqueProfiles = set()
    for key in profileSets:
        for value in profileSets[key]:
            uniqueProfiles.add(value)
    if(sentences):
        for currentSentence in sentences:
            for currentWord in currentSentence.split(' '):
                if currentWord not in wordsFoundInCurrentSentence:
                        for aProfile in uniqueProfiles:
                            if(aProfile == currentWord):
                                wordsFoundInCurrentSentence.append(currentWord)
                                if(aProfile not in profileDict):
                                    newProfileWord = Profile(currentWord)
                                    newProfileWord = addAssociatedWords(currentSentence, newProfileWord, commonWords)
                                    profileDict[currentWord] = newProfileWord
                                else:
                                    addAssociatedWords(currentSentence,profileDict[aProfile], commonWords)
                wordsFoundInCurrentSentence = []
    return profileDict

#Opens text and set files, with error handling
def fileRead(corpus_file_name, test_sets_file, commonwords_file_name = None):
    dictionaryKeys = {}
    try:
        sentences = openFile(corpus_file_name)
        profileSets = createSets(test_sets_file)
        
        #If sentences and profiles exist, read common words file
        if(sentences and profileSets):
            commonWords = readCommonWordsFile(commonwords_file_name);
            profileDict = getAllProfiles(sentences, profileSets,commonWords)
            endValue = 0
            
            #Compare two profiles
            if(profileSets):
                for key in profileSets:
                    dictonaryAllValue = {}
                    if(key in profileDict):
                        for value in list(profileSets[key][1:]):
                                if(value in profileDict):
                                    endValue = compareTwoProfiles(profileDict[profileSets[key][0]], profileDict[value])
                                else:
                                    endValue = 0
                                dictonaryAllValue[value] = endValue
                        dictionaryKeys[key] = dictonaryAllValue
                    else:
                        print("Key: " + key + " Was not found in text file:")
        
        #Error handling (if text and set files are empty)
        else:
            numSentences = len(sentences)
            numProfiles = len(profileSets)
            if  (numSentences == 0 and numProfiles == 0):
                print("Error: textfile and set file are both empty")
            elif numSentences == 0:
                print("Error: text file is empty")
            elif numProfiles == 0:
                print("Error: set file is empty")
                
        #Print sysnonym for target word is set file
        for keys in dictionaryKeys:
            print(keys + "\n")
            dictionaryKeys[keys] = sorted(dictionaryKeys[keys].items(), key =lambda kv,: kv[1], reverse = True)
            if(dictionaryKeys[keys]):
                for value in dictionaryKeys[keys]:
                    print("\t " + value[0] + "\t" + str(value[1]))
                print("\nSynonym for " + keys + " is " + str(dictionaryKeys[keys][0][0]) + "\n")
            else:
                 print("No synonym for " + keys + "\n check set file\n")
    except IOError as e:
        print(str(e))
  
#main function
def main(corpus_file_name, test_sets_file, commonwords_file_name = None):
    start_time = time.time()
    fileRead(corpus_file_name, test_sets_file, commonwords_file_name)
    
    #Prints computational time of program
    print("--- %s seconds ---" % (time.time() - start_time))

#main()
#Tested with
main("sample.txt","set.txt","common.txt")
#with files from project description