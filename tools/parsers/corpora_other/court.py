from tools.parsers import basecorpus
import pandas as pd

# this class reads Supreme Court historic data
class Court(basecorpus.BaseCorpus):
    # constructor
    def __init__(self):
        basecorpus.BaseCorpus.__init__(self)
        self.defaultFileNameOrig = '.'+self.sepDir+'corpora'+self.sepDir+'washington-law'+self.sepDir+'justice_centered_docket_post2000.csv'


    # reads the file and returns pandas DataFrame
    def readFileRaw(self, rawFileName ):
        if rawFileName == None:
            rawFileName = self.defaultFileNameOrig

        with open(rawFileName, 'r') as rawfile:
            data = pd.read_csv(rawfile, sep=",", skipinitialspace = True)
            filterData.fillna(value = "") # replace empty values

            return filterData
        return None # just safety measurement
