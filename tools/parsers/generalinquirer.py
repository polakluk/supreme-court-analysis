from tools.parsers import basecorpus
import pandas as pd

# this class reads General Inquirer corpus and turns it into a proper CSV file
class GeneralInquirer(basecorpus.BaseCorpus):
    # constructor
    def __init__(self):
        self.defaultFileNameOrig = './corpora/general-inquirer/general-inquirer.txt'
        self.defaultFileNameProcessed = './corpora/general-inquirer/general-inquirer-new.csv'
        self.filterHeader = ['entry', # word
                            'positiv', # clearly positive words (except for 'yes' words)
                            'negativ', # clearly negative words (except for 'no' words)
                            'active', # words with active orientation
                            'passive', # words with passive orientation
                            'affil', # positive words which express supportiveness
                            'hostile', # negative words which express hostility
                            'strong', # words which imply strength
                            'power', # words which imply strength and indicate concern with power
                            'weak', # words which imply weakness
                            'submit', # words which imply weakness and indicate connoting submission to authority
                            'yes', # yes words
                            'no', # no words
                            'negate', # words which negate meaning
                            'intrj', # words which include exclamations
                            'pleasur', # words indicating enjoyment
                            'pain', # words indicating suffering
                            'feel', # words indicating particular feelings
                            'need', # words indicating expression of need and interest
                            'persist', # words indicating endurance in action
                            'othtags'
                            ]


    # reads the file and returns pandas DataFrame
    def readFileRaw(self, rawFileName ):
        if rawFileName == None:
            rawFileName = self.defaultFileNameOrig
        skippedFirstLine = False

        with open(rawFileName, 'r') as rawfile:
            data = pd.read_csv(rawfile, sep="\t", skipinitialspace = True).rename(columns=str.lower)
            filterData = data[self.filterHeader].set_index(['entry', 'othtags']).dropna(how='all') # drop unused rows (that's why entry is made index for rows)
            filterData.fillna(value = "") # replace empty values
            filterData['entry'] = [rec[0] for rec in filterData.index.values ]  # now, entry can be turned back into a column
            filterData['othtags'] = [rec[1] for rec in filterData.index.values ]  # now, even ontho tags can be turned back into a column
            filterData.reset_index(inplace = True, drop = True ) # and index for rows can be dropped

            # escape sharp postfixes from entries
            filterData['entry'] = filterData['entry'].map(lambda cell: (cell.split('#'))[0] if '#' in cell else cell)

            # convert everything to lowercase
            for col in self.filterHeader:
                filterData[col] = filterData[col].map(lambda cell: cell if type(cell)!=str else cell.lower())

            return filterData
        return None # just safety measurement
