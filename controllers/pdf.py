import controllers.base

# my tools
from tools.parsers import pdf as pdfParser
from tools.parsers import tesseractocr as TesseractParser
from tools.cleaners import basic
from tools.dialogs import extractor
from tools.dialogs import container as dialogContainer
from tools.dialogs import posdialog as dialogPosDialog
from tools.dialogs import sentencedialog as dialogSentenceDialog
from tools.pos import nltkpos as nltkPos
from tools.pos import textblobpostagger as textBlobPosTagger

# Controller for handling work with PDFs
class Pdf(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'read-pdf': self._readPdfFile, # step 1
                                'process-pdf' : self._preprocessInputFile, # step 2
                                'extract-parts' : self._extractPartsDialog, # step 3
                                'generate-sentences' : self._generate_sentences, # step 4a
                                'generate-pos' : self._generatePosTags # step 4b
        }


    # initializes its own parser
    def initializeArgumentParser(self):
        # extract input file name
        self.argParser.add_argument('-f', help="Filename", dest="filename", required=True)
        self.argParser.add_argument('-m', help="PDF mode", dest="mode", required = False)
        self.parserInitialized = True


    # read PDF file
    def _readPdfFile(self):
        args = self.argParser.parse_args()
        fileName = args.filename
    #	currentParser = pdfParser.Pdf(".\\parsed-data\\")
    	currentParser = TesseractParser.TesseractOcr(self.parsedDataDir)
    	currentParser.readFile(fileName, args['mode'])


    # clean up read file afterwards
    def _preprocessInputFile(self):
        args = self.argParser.parse_args()
        fileName = args.filename
    	cleaner = basic.Basic(self.parsedDataDir);
    	cleaner.cleanUp(fileName);


    # extracts parts of dialog from clean file and later saves them
    def _extractPartsDialog(self):
        args = self.argParser.parse_args()
        fileName = args.filename
    	with open(fileName, "r") as cleanFile:
    		extractTool = extractor.Extractor(self.parsedDataDir, False)
    		dialogParts = extractTool.Extract(cleanFile.read())
    		extractTool.SaveToFile(dialogParts, fileName)


    # this part puts POS tags to loaded file and saves them for later use
    def _generatePosTags(self):
        args = self.argParser.parse_args()
        fileName = args.filename
        posTagger = textBlobPosTagger.TextBlobPosTagger()

    	dialogSent = dialogSentenceDialog.SentenceDialog(self.parsedDataDir, self.debug)
    	dialogSent.LoadFromFile(fileName)

    	dialogPos = dialogPosDialog.PosDialog(self.parsedDataDir, self.debug)
    	dialogPos.SetDialogSent(dialogSent)
    	dialogPos.SetPosTagger(posTagger)
    	data = dialogPos.GetPosTaggedParts()
        if self.debug:
    		self.pprint.pprint(data)
    	dialogPos.SaveToFile(fileName)


    # this method generates sentences from turn
    def _generate_sentences(self):
        args = self.argParser.parse_args()
        fileName = args.filename
        posTagger = textBlobPosTagger.TextBlobPosTagger()

    	dialog = dialogContainer.Container()
    	dialog.LoadFromFile(fileName)

    	dialogSent = dialogSentenceDialog.SentenceDialog(self.parsedDataDir, self.debug)
    	dialogSent.SetDialog(dialog)
    	dialogSent.SetPosTagger(posTagger)
    	data = dialogSent.SplitTurnsToSentences()
        if self.debug:
    		self.pprint.pprint(data)
    	dialogSent.SaveToFile(fileName)
