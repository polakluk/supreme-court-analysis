import pandas as pd
import csv

# this class reads a corpus and turns it into a proper CSV file
class BaseCorpus(object):

    # saves the data with header to a file in CSV format
    def saveFileCsv(self, data, fileName):
        if fileName == None:
            fileName = self.defaultFileNameProcessed
        with open(fileName, 'wb') as csvfile:
            data.to_csv(csvfile, index = False)


    # reads the data from CSV file and returns pandas DataFrame
    def readFileCsv(self, fileName):
        if fileName == None:
            fileName = self.defaultFileNameProcessed
        with open(fileName, 'r') as csvfile:
            data = pd.read_csv(csvfile)
            return data
