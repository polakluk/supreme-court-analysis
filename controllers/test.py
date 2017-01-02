import controllers.base
from os import walk
import re
import pandas as pd
from tools.dialogs import extractor
from tools.parsers.pdf import tesseractocr as TesseractParser

class Test(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'test' : self._test,
                                'test2' : self._test_2,
        }

    def _run_update(self, row, colName, colRole):
        row[colName] = extractor.Extractor.fixNames(row[colName], row[colRole])
        return row

    # method for testing code and short experiments
    def _test_2(self):
        list_processed = ['features', 'sentiment', 'sentences', 'pos', 'dialog']
        for (dirpath, dirnames, filenames) in walk(self.parsedDataDir):
            for f_name in list_processed:
                for dir_name in dirnames:
                    df = pd.read_csv(dirpath+dir_name+self.pathSeparator+dir_name+'.'+f_name)
                    if 'Name' in df.columns:
                        df = df.apply(lambda row: self._run_update(row, 'Name', 'Role'), axis = 1)
                    elif 'name' in df.columns:
                        df = df.apply(lambda row: self._run_update(row, 'name', 'role'), axis = 1)
                    df.to_csv(dirpath+dir_name+self.pathSeparator+dir_name+'.'+f_name, index=False)

    def _test(self):
        self.__parser_pdf = TesseractParser.TesseractOcr(self.parsedDataDir )
        self.__parser_pdf.testPdf('./img_60.png') #readFileAdvanced('.\\arguments\\bottom-middle\\12-1497_6k37.pdf', 'bottom-middle')
