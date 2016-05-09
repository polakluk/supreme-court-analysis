import controllers.base

# my tools
from tools.parsers import pdf as pdfParser
from tools.parsers import tesseractocr as TesseractParser
from tools.cleaners import basic
from tools.dialogs import extractor
from tools.dialogs import container as dialogContainer
from tools.dialogs import posdialog as dialogPosDialog
from tools.pos import nltkpos as nltkPos

# Controller for handling work with PDFs
class Pdf(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'read-pdf': self._readPdfFile,
                                'process-pdf' : self._preprocessInputFile,
                                'extract-parts' : self._extractPartsDialog,
                                'generate-pos' : self._generatePosTags
        }


    # initializes its own parser
    def initializeArgumentParser(self):
        # extract input file name
        self.argParser.add_argument('-f', help="Filename", dest="filename", required=True)
        self.parserInitialized = True


    # read PDF file
    def _readPdfFile(self):
        args = self.argParser.parse_args()
        fileName = args.filename
    #	currentParser = pdfParser.Pdf(".\\parsed-data\\")
    	currentParser = TesseractParser.TesseractOcr(self.parsedDataDir)
    	currentParser.readFile(fileName)


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
    	posTagger = nltkPos.NltkPos()

    	dialog = dialogContainer.Container()
    	dialog.LoadFromFile(fileName)

    	dialogPos = dialogPosDialog.PosDialog(self.parsedDataDir, self.debug)
    	dialogPos.SetDialog(dialog)
    	dialogPos.SetPosTagger(posTagger)
    	data = dialogPos.GetPosTaggedParts()
        if self.debug:
    		self.pprint.pprint(data)
    	dialogPos.SaveToFile(fileName)
