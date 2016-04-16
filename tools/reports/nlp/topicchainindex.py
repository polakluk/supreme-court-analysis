import csv

from nltk import word_tokenize
from tools.dialogs import person as personDialog

# this class prepares reports from loaded dialog
# REPORT Description:
# The report returns list of topic chain indices for selected person and subset of words
class TopicChainIndex:

    # constructor
    def __init__(self, reportsDir):
        self.__outputDir = reportsDir
        self.__dialog = None


    # sets dialog for this report
    def SetDialog(self, newDialog):
        self.__dialog = newDialog


    # returns list of TCI indices for selected person
    # words - list of list of words;
    # TCI index is calcuolated by the relative distance betwen first mention of a word from list of words and the last mention of any of those words
    def CalculateTciPerson(self, personName, personRole, listWords):
        people = personDialog.Person()
        # dont do anything unless everything is properly set up
        parts = self.__dialog.GetDialog()
        if parts == None:
            return None

        # calculate position of each part in dialog
        return [ {'word' : words[0], 'result' : self._calculateTciWordPerson(personName, personRole, words, parts)} for words in listWords]


    # saves the report to file
    def SaveToFile(self, personName, personRole, data, name = None):
        fileName = 'tci_'+personName+'.csv'
        if name != None:
            fileName = name + '_' + personName + ".csv"

        with open(self.__outputDir + fileName, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerow(['Role', 'Name', 'Noun', 'Count', 'Start', 'Last', 'Length'])
            for record in data:
                writer.writerow([personRole, personName, record['word'], record['result']['count'], record['result']['startPos'], record['result']['lastPos'], record['result']['length']])


    # this method calculates TCI for one list of words for one
    def _calculateTciWordPerson(self, personName, personRole, words, parts):
        count = 0
        startPos = -1
        lastPos = -1
        actPos = -1
        for part in parts:
            actPos = part['positions']['dialog']
            if self._wordInDialogPart(part, personName, personRole, words):
                count += 1
                lastPos = actPos
                if startPos == -1:
                    startPos = actPos

        return {'count' : count, 'startPos' : startPos, 'lastPos' : lastPos, 'length' : (lastPos - startPos)}


    # checks, if any word from the list is present in this dialog part
    # also, it checks, if this part belongs to the person we are interested in (if not, then return False)
    def _wordInDialogPart(self, part, personName, role, words):
        result = False
        # check, if  this part of dialog belongs to the person we are interedted in
        if part['role'] != role or part['name'] != personName:
            return result

        # check, if any word is in the dialog
        textWords = [w.upper() for w in word_tokenize(part['text'])]
        return any( [ (w.upper() in textWords) for w in words])
