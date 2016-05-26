import controllers.base
import pandas as pd

# my tools
from tools.parsers import mpqa as mpqaParser
from tools.parsers import mpqaprocessed as mpqaProcessedParser
from tools.parsers import generalinquirer as generalInquirerParser

# Controller for handling work with MPQA corpus
class Mpqa(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'read-corpus-sentences-raw': self._readCorpusSentencesRaw,
                                'read-corpus-annotations-raw' : self._readCorpusAnnotationsRaw,
                                'read-corpus-processed-clues' : self._readCorpusProcessedClues,
                                'combine-corpora-clues' : self._combineCorporaClues,
        }


    # initializes its own parser
    def initializeArgumentParser(self):
        # extract input file name
        self.argParser.add_argument('-f', help="Input Filename", dest="filename", required = False)
        self.argParser.add_argument('-fout', help="Output Filename", dest="outputFile", required = False)
        self.parserInitialized = True


    # reads MPQA corpus and saves it in format easier to read
    def _readCorpusSentencesRaw(self):
        parser = mpqaParser.Mpqa()
        args = vars(self.argParser.parse_args())
        data = parser.readAllFilesSentences()
        if self.debug:
            self.pprint.pprint("Read sentences: " + str(len(data)))
        parser.saveFileCsv(data, args['outputFile'])
        self.pprint.pprint("MPQA corpus sentences parsed and saved!")


    # reads MPQA corpus from obtained from Github and saves it in format easier to read
    def _readCorpusProcessedClues(self):
        parser = mpqaProcessedParser.MpqaProcessed()
        args = vars(self.argParser.parse_args())
        data = parser.readFileRaw(args['filename'])
        parser.saveFileCsv(data, args['outputFile'])
        self.pprint.pprint("Preprocessed corpus parsed and saved!")


    # combine my selected data  from Generic Inquirer with data obtained from Github
    def _combineCorporaClues(self):
        parserMpqa = mpqaProcessedParser.MpqaProcessed()
        parserInquirer = generalInquirerParser.GeneralInquirer()
        dataMpqa = parserMpqa.readFileCsv(None)
        dataInquirer = parserInquirer.readFileCsv(None)
        parserInquirer.CombineDictionaries(dataMpqa, dataInquirer)


    # reads annotations from MPQA corpus and adds them to already parsed data
    def _readCorpusAnnotationsRaw(self):
        parser = mpqaParser.Mpqa()
        args = vars(self.argParser.parse_args())
        data = parser.readAllFilesAnnotations()
        if self.debug:
            self.pprint.pprint("Read annotations: " + str(len(data)))
        parser.saveFileCsvAnnotations(data, args['outputFile'])
        self.pprint.pprint("MPQA corpus sentences parsed and saved!")