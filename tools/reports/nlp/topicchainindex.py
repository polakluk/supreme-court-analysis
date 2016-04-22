import csv
import collections

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
        self.__tthreshold = 2 # threshold for nouns which should be used for TCI computation


    # sets dialog for this report
    def SetDialog(self, newDialog):
        self.__dialog = newDialog

    # sets threshold for used nouns
    def SetThreshold(self, threshold):
        self.__threshold = threshold


    # returns list of TCI indices
    # param nouns - Result of report UsedNounsPerson
    def CalculateTci(self, nouns):
        people = personDialog.Person()
        # dont do anything unless everything is properly set up
        parts = self.__dialog.GetDialog()
        if parts == None:
            return None

        # now, get list of words which we want to check
        listWords = []
        [[ listWords.append(noun) for noun in nouns[key]['nouns']] for key in nouns.keys()]
        # count duplicates together
        hashWords = collections.defaultdict(int)
        for noun in listWords:
            hashWords[noun[0]] += noun[1]
        # sort them by count of each noun and filter them out by threshold
        listWords = sorted([(key, hashWords[key]) for key in hashWords.keys()], key = lambda x: x[1], reverse = True)
        listWords = [word for word in listWords if word[1] >= self.__threshold]

        # calculate position of each part in dialog
        results = [ {'word' : word[0],
                    'result' : self._calculateTciWord(word[0], parts)} for word in listWords]
        # test, if any word was found
        if sum([r['result']['length'] for r in results]) == 0:
            return None # No, no word has been foudn

        results.sort(key = lambda x: x['result']['length'], reverse = True)
        return results


    # saves the report to file
    def SaveToFile(self, data, name = None):
        fileName = 'tci_'+str(self.__threshold)+'.csv'
        if name != None:
            fileName = name + "_" + str(self.__threshold) + ".csv"

        with open(self.__outputDir + fileName, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerow(['Noun', 'Count', 'Start', 'Last', 'Length'])
            if data != None:
                for record in data:
                    writer.writerow([record['word'], record['result']['count'], record['result']['startPos'], record['result']['lastPos'], record['result']['length']])
            else:
                print("No data for - " + fileName)


    # this method calculates TCI for one word
    def _calculateTciWord(self, word, parts):
        count = 0
        startPos = -1
        lastPos = -1
        actPos = -1
        for part in parts:
            actPos = part['positions']['dialog']
            isPart = any(([w.upper() == str(word).upper() for w in word_tokenize(part['text'])]))
            if isPart:
                count += 1
                lastPos = actPos
                if startPos == -1:
                    startPos = actPos
        return {'count' : count, 'startPos' : startPos, 'lastPos' : lastPos, 'length' : (lastPos - startPos)}
