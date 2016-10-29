import csv
import collections

from nltk import word_tokenize
from tools.dialogs import person as personDialog

# this class prepares reports from loaded dialog
# REPORT Description:
# The report returns list of topic chain indices for selected person and subset of words
class TopicChainIndex(object):

    # constructor
    def __init__(self, reportsDir):
        self._outputDir = reportsDir
        self._dialog = None
        self._dialog_pos = None
        self._threshold = 2  # threshold for nouns which should be used for TCI computation
        self._synonym_provider = None


    # sets dialog for this report
    def SetDialog(self, newDialog):
        self._dialog = newDialog


    # sets POS dialog for this report
    def SetDialogPos(self, newDialog):
        self._dialog_pos = newDialog


    # sets threshold for used nouns
    def SetThreshold(self, threshold):
        self._threshold = threshold

    # sets synonym provider
    def SetSynonymProvider(self, provider):
        self._synonym_provider = provider


    # returns list of TCI indices
    # param nouns - Result of report UsedNounsPerson
    def CalculateTci(self, nouns):
        # dont do anything unless everything is properly set up
        parts = self._dialog.GetDialog()
        if parts is None:
            return None

        # filter words by threshold
        listWords = [word[0] for word in nouns if word[1] >= self._threshold]

        # calculate position of each part in dialog
        results = [ {'word': word,
                    'result': self._calculateTciWord(word, parts)} for word in listWords]
        # test, if any word was found
        if sum([r['result']['length'] for r in results]) == 0:
            return None # No, no word has been found

        results.sort(key=lambda x: x['result']['length'], reverse=True)
        return results


    # saves the report to file
    def SaveToFile(self, data, name=None):
        fileName = 'tci_'+str(self._threshold)+'.csv'
        if name != None:
            fileName = name + "_" + str(self._threshold) + ".csv"

        with open(self._outputDir + fileName, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
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
        for part in parts:
            actPos = part['positions']['dialog']
            isPart = False
            if self._synonym_provider is None:
                isPart = any(([w.upper() == str(word).upper() for w in word_tokenize(part['text'])]))
            else:
                words = self._synonym_provider.GetSynonyms(word)
                for w_s in words:
                    isPart = any(([w.upper() == str(w_s).upper() for w in word_tokenize(part['text'])]))
                    if isPart:
                        break
            if isPart:
                count += 1
                lastPos = actPos
                if startPos == -1:
                    startPos = actPos
        return {'count': count, 'startPos': startPos, 'lastPos': lastPos, 'length': (lastPos - startPos)}
