from tools.parsers import basecorpus
import pandas as pd
import numpy as np

# this class reads MPQA corpus subjective clues and turns them into a proper CSV file
class MpqaProcessed(basecorpus.BaseCorpus):
    # constructor
    def __init__(self):
        basecorpus.BaseCorpus.__init__(self)
        self.defaultFileNameOrig = '.'+self.sepDir+'corpora'+self.sepDir+'mpqa-clues'+self.sepDir+'subjectivity-clues.txt'
        self.defaultFileNameProcessed = '.'+self.sepDir+'corpora'+self.sepDir+'mpqa-clues'+self.sepDir+'subjectivity-clues-new.csv'
        self.columns = ['entry', 'type', 'pos', 'stemmed', 'priorpolarity']


    # reads the file and returns pandas DataFrame
    def readFileRaw(self, rawFileName ):
        if rawFileName == None:
            rawFileName = self.defaultFileNameOrig
        skippedFirstLine = False

        with open(rawFileName, 'r') as rawFile:
            lines = rawFile.readlines()
            data = pd.DataFrame( index = np.arange(0, len(lines) - 1), columns = self.columns )
            idx = 0
            for line in lines:
                parts = [ part.split('=') for part in line.split(' ')]
                if len(parts) == 6: # is this an ordinary row?
                    data.loc[idx] = [parts[2][1], parts[0][1], parts[3][1], parts[4][1], parts[5][1].strip()]
                else: # nope, for some reason this row has a different format
                    if len(parts[5]) == 1:
                        data.loc[idx] = [parts[2][1], parts[0][1], parts[3][1], parts[4][1], parts[6][1].strip()]
                    else:
                        if parts[2][0] == 'len':
                            data.loc[idx] = [parts[3][1], parts[0][1], parts[4][1], parts[5][1], parts[6][1].strip()]
                idx += 1

            return data
        return None # just safety measurement
