# needed
import os
import sys
import getopt
import pprint

# my tools
from tools.parsers import pdf as pdfParser
from tools.parsers import tesseractocr as TesseractParser
from tools.cleaners import basic
from tools.dialogs import extractor
from tools.dialogs import container as dialogContainer

#reports
from tools.reports import turns as turnsReport
from tools.reports import follow as followReport
from tools.reports import followratio as followRatioReport
from tools.reports import mostfollow as mostFollowReport

# read PDF file
def readPdfFile(fileName):
#	currentParser = pdfParser.Pdf(".\\parsed-data\\")
	currentParser = TesseractParser.TesseractOcr("."+os.path.sep+"parsed-data"+os.path.sep)
	currentParser.readFile(fileName)	

# clean up read file afterwards
def preprocessInputFile(fileName):
	cleaner = basic.Basic("."+os.path.sep+"parsed-data"+os.path.sep);
	cleaner.cleanUp(fileName);

# extracts parts of dialo from clean file and later saves the,
def extractPartsDialog(fileName):
	pp = pprint.PrettyPrinter(indent = 4 )

	with open(fileName, "r") as cleanFile:
		extractTool = extractor.Extractor(False)
		dialogParts = extractTool.Extract(cleanFile.read())

		dialog = dialogContainer.Container()
		dialog.SetDialog(dialogParts)

#		report1 = turnsReport.Turns("."+os.path.sep+"report-data"+os.path.sep)
#		report1.SetDialog(dialog)
#		print ( report1.Turns() )

#		report2 = followReport.Follow("."+os.path.sep+"report-data"+os.path.sep)
#		report2.SetDialog(dialog)
#		print ( report2.Follows() )

#		report3 = followRatioReport.FollowRatio("."+os.path.sep+"report-data"+os.path.sep)
#		report3.SetDialog(dialog)
#		report3.SetInterval(0.2, 0.5)
#		print ( report3.CalculateFollowRatio() )

		report4 = mostFollowReport.MostFollow("."+os.path.sep+"report-data"+os.path.sep)
		report4.SetDialog(dialog)
		report4.SetInterval(0.2, 0.7)
		pp.pprint ( report4.MostFollows() )


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