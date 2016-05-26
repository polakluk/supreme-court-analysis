from tools.parsers import basecorpus
import pandas as pd
import numpy as np

# this class reads list of negation words and transforms them into a proper CSV with their upper case representation
class Negation(basecorpus.BaseCorpus):
    # constructor
    def __init__(self):
        basecorpus.BaseCorpus.__init__(self)
        self.defaultFileNameOrig = '.'+self.sepDir+'corpora'+self.sepDir+'negations'+self.sepDir+'negations.txt'
        self.defaultFileNameProcessed = '.'+self.sepDir+'corpora'+self.sepDir+'processed'+self.sepDir+'negation.csv'
        self.columns = ['phrase', 'phraseUpper']


    # reads the file and returns pandas DataFrame
    def readFileRaw(self, rawFileName ):
        if rawFileName == None:
            rawFileName = self.defaultFileNameOrig
        skippedFirstLine = False

        with open(rawFileName, 'r') as rawfile:
            data = pd.read_csv(rawfile, sep="\t", skipinitialspace = True).rename(columns=str.lower)
            processedData = pd.DataFrame(np.zeros((data.shape[0], 2)), columns = self.columns)
            processedData['phrase'] = data
            processedData['phraseUpper'] = processedData['phrase'].map(lambda cell: cell.upper())
            return processedData
        return None # just safety measurement