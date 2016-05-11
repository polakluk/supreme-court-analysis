import controllers.base

from tools.parsers import mpqaprocessed as mpqaProcessedParser

# my tools

# Controller for handling work with MPQA corpus
class Mpqa(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'read-corpus-raw': self._readCorpusRaw,
                                'read-corpus-processed' : self._readCorpusProcessed
        }


    # initializes its own parser
    def initializeArgumentParser(self):
        # extract input file name
        self.argParser.add_argument('-f', help="Input Filename", dest="filename", required = False)
        self.argParser.add_argument('-fout', help="Output Filename", dest="outputFile", required = False)
        self.parserInitialized = True


    # reads MPQA corpus and saves it in format easier to read
    def _readCorpusRaw(self):
        self.pprint.pprint("asfsdf")


    def _readCorpusProcessed(self):
        parser = mpqaProcessedParser.MpqaProcessed()
        args = vars(self.argParser.parse_args())
        data = parser.readFileRaw(args['filename'])
        parser.saveFileCsv(data, args['outputFile'])
        self.pprint.pprint("Preprocessed corpus parsed and saved!")
