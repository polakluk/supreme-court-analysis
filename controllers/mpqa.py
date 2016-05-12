import controllers.base
import pandas as pd

# my tools
from tools.parsers import mpqaprocessed as mpqaProcessedParser
from tools.parsers import generalinquirer as generalInquirerParser

# Controller for handling work with MPQA corpus
class Mpqa(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'read-corpus-raw': self._readCorpusRaw,
                                'read-corpus-processed' : self._readCorpusProcessed,
                                'combine-corpora' : self._combineCorpora,
        }
        self.combinedFileLoc = self.corporaDir + "processed" + self.pathSeparator + 'combined-mpqagithub-gi.csv'


    # initializes its own parser
    def initializeArgumentParser(self):
        # extract input file name
        self.argParser.add_argument('-f', help="Input Filename", dest="filename", required = False)
        self.argParser.add_argument('-fout', help="Output Filename", dest="outputFile", required = False)
        self.parserInitialized = True


    # reads MPQA corpus and saves it in format easier to read
    def _readCorpusRaw(self):
        self.pprint.pprint("asfsdf")


    # reads MPQA corpus from obtained from Github and saves it in format easier to read
    def _readCorpusProcessed(self):
        parser = mpqaProcessedParser.MpqaProcessed()
        args = vars(self.argParser.parse_args())
        data = parser.readFileRaw(args['filename'])
        parser.saveFileCsv(data, args['outputFile'])
        self.pprint.pprint("Preprocessed corpus parsed and saved!")


    # combine my selected data  from Generic Inquirer with data obtained from Github
    def _combineCorpora(self):
        parser_mpqa = mpqaProcessedParser.MpqaProcessed()
        parser_inquirer = generalInquirerParser.GeneralInquirer()
        data_mpqa = parser_mpqa.readFileCsv(None)
        data_inquirer = parser_inquirer.readFileCsv(None)

        data = pd.merge(data_inquirer, data_mpqa, on= 'entry')
        with open(self.combinedFileLoc, 'wb') as csvfile:
            data.to_csv(csvfile, index = False)
