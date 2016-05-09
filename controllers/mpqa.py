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
class Mpqa(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        super(basecontroller.Base, self).__init__(pprinter, argParse)
        self.availableTask = {
                                'read-corpus': self._readCorpus,
        }

    # reads MPQA corpus and saves it in format easier to read
    def __readCorpus(self):
        pass
