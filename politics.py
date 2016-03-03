# needed
import os
import sys
import getopt
from tools.parsers import pdf as pdfParser
from tools.parsers import tesseractocr as TesseractParser
from tools.cleaners import basic
from tools.dialogs import extractor

# read PDF file
def readPdfFile(fileName):
#	currentParser = pdfParser.Pdf(".\\parsed-data\\")
	currentParser = TesseractParser.TesseractOcr("."+os.path.sep+"parsed-data"+os.path.sep)
	currentParser.readFile(fileName)	

# clean up read file afterwards
def preprocessInputFile(fileName):
	cleaner = basic.Basic("."+os.path.sep+"parsed-data"+os.path.sep);
	cleaner.cleanUp(fileName);

def extractPartsDialog(fileName):
	with open(fileName, "r") as cleanFile:
		extractTool = extractor.Extractor(True)
		extractTool.Extract(cleanFile.read())

# main
def main(argv):

	mode = (int)(argv[1])

	execute = {
		0 : readPdfFile,
		1 : preprocessInputFile,
		2 : extractPartsDialog
	}

	execute[mode](argv[2]);
	return 0

if __name__ == '__main__': sys.exit(main(sys.argv)) 