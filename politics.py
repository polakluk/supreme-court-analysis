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
from tools.pos import nltkpos as nltkPos

# frequency reports
from tools.reports import turns as turnsReport
from tools.reports import follow as followReport
from tools.reports import followratio as followRatioReport
from tools.reports import mostfollow as mostFollowReport
from tools.reports import turnspositionlength as turnsPositionLengthReport

# nlp reports
from tools.reports import nounphrases as nounPhrasesReport

# read PDF file
def readPdfFile(fileName):
#	currentParser = pdfParser.Pdf(".\\parsed-data\\")
	currentParser = TesseractParser.TesseractOcr("."+os.path.sep+"parsed-data"+os.path.sep)
	currentParser.readFile(fileName)

# clean up read file afterwards
def preprocessInputFile(fileName):
	cleaner = basic.Basic("."+os.path.sep+"parsed-data"+os.path.sep);
	cleaner.cleanUp(fileName);

# extracts parts of dialo from clean file and later saves them
def extractPartsDialog(fileName, isDebug = True):
	with open(fileName, "r") as cleanFile:
		extractTool = extractor.Extractor("."+os.path.sep+"parsed-data"+os.path.sep, False)
		dialogParts = extractTool.Extract(cleanFile.read())
		extractTool.SaveToFile(dialogParts, fileName)


def generateReports(fileName, isDebug = True):
	pp = pprint.PrettyPrinter(indent = 4 )
	dialog = dialogContainer.Container()
	dialog.LoadFromFile(fileName)

	report1 = turnsReport.Turns("."+os.path.sep+"report-data"+os.path.sep)
	report1.SetDialog(dialog)
	data = report1.Turns()
	if isDebug:
		print("############ Report #1 - Most Turns")
		pp.pprint(data)
	report1.SaveToFile(data)

	report2 = followReport.Follow("."+os.path.sep+"report-data"+os.path.sep)
	report2.SetDialog(dialog)
	data = report2.Follows()
	if isDebug:
		print
		print
		print("############ Report #2 - Follows")
		pp.pprint(data)
	report2.SaveToFile(data)

	report3 = followRatioReport.FollowRatio("."+os.path.sep+"report-data"+os.path.sep)
	report3.SetDialog(dialog)
#	report3.SetInterval(0.2, 0.5)
	data = report3.CalculateFollowRatio()
	if isDebug:
		print
		print
		print("############ Report #3 - Follow Ratio")
		pp.pprint(data)
	report3.SaveToFile(data)

	report4 = mostFollowReport.MostFollow("."+os.path.sep+"report-data"+os.path.sep)
	report4.SetDialog(dialog)
	report4.SetInterval(0.2, 0.7)
	data = report4.MostFollows()
	if isDebug:
		print
		print
		print("############ Report #4 - Most Follow")
		pp.pprint(data)
	report4.SaveToFile(data)

	report5 = turnsPositionLengthReport.TurnsPositionLength("."+os.path.sep+"report-data"+os.path.sep)
	report5.SetDialog(dialog)
#		report5.SetInterval(0.2, 0.7)
	data = report5.AllTurns()
	if isDebug:
		print
		print
		print("############ Report #5 - Turns with Position and Length")
		pp.pprint(data)
	report5.SaveToFile(data)


def nlpReports(fileName):
	pp = pprint.PrettyPrinter(indent = 4 )
	dialog = dialogContainer.Container()
	dialog.LoadFromFile(fileName)

	posTagger = nltkPos.NltkPos()
	report1 = nounPhrasesReport.NounPhrases("."+os.path.sep+"report-data"+os.path.sep)
	report1.SetDialog(dialog)
	report1.SetPosTagger(posTagger)
	report1.ExtractNounPhrases()


# main
def main(argv):

	mode = (int)(argv[1])

	execute = {
		0 : readPdfFile,
		1 : preprocessInputFile,
		2 : extractPartsDialog,
		3 : generateReports,
		4 : nlpReports
	}

	execute[mode](argv[2]);
	return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
