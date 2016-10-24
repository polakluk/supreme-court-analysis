import controllers.base

# my tools
from tools.parsers.corpora_sentiment import generalinquirer as generalInquirerParser

# Controller for handling work with General Inquirer corpus
class Inquirer(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'read-corpus-raw': self._readCorpusRaw,
                                'read-corpus' : self._readCorpusCsv
        }


    # initializes its own parser
    def initializeArgumentParser(self):
        # extract input file name
        self.argParser.add_argument('-f', help="Input Filename", dest="filename", required = False)
        self.argParser.add_argument('-fout', help="Output Filename", dest="outputFile", required = False)
        self.parserInitialized = True


    # reads General Inquirer corpus and saves it in format easier to read
    def _readCorpusRaw(self):
        parser = generalInquirerParser.GeneralInquirer()
        args = vars(self.argParser.parse_args())

        data = parser.readFileRaw(args['filename'])
        parser.saveFileCsv(data, args['outputFile'])
        self.pprint.pprint("Corpus parsed and saved!")


    # test method to check, if General Inquirer data are accessible
    def _readCorpusCsv(self):
        parser = generalInquirerParser.GeneralInquirer()
        args = vars(self.argParser.parse_args())

        data = parser.readFileCsv(args['filename'])
        self.pprint.pprint(data)
