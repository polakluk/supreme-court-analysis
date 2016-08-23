import controllers.base
import os

# my tools
from tools.filehelper import FileHelper
from tools.cleaners import basic
from tools.parsers import tesseractocr as TesseractParser
from tools.dialogs import extractor
from tools.dialogs import container as dialogContainer
from tools.dialogs import posdialog as dialogPosDialog
from tools.dialogs import sentencedialog as dialogSentenceDialog
from tools.pos import nltkpos as nltkPos
from tools.pos import textblobpostagger as textBlobPosTagger
from tools.dialogs import helper as dialogHelper
from tools.synonyms import wordnet as wordnetSyns
from tools.synonyms import lin as wordnetLinSyns

# frequency reports
from tools.reports import turns as turnsReport
from tools.reports import follow as followReport
from tools.reports import followratio as followRatioReport
from tools.reports import mostfollow as mostFollowReport
from tools.reports import turnspositionlength as turnsPositionLengthReport
from tools.reports import mostwords as mostWordsReport

# nlp reports
from tools.reports.nlp import nounphraseparts as nounPhrasePartsReport
from tools.reports.nlp import usednounsperson as usedNounsPersonReport
from tools.reports.nlp import topicchainindex as topicChainIndexReport
from tools.reports.nlp import groupsynonymstci as groupSynonymsTciReport


# Controller that can trigger whole pipeline with one command from command-line
class Pipeline(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'all-tasks': self._allTasks,
        }


    # initializes its own parser
    def initializeArgumentParser(self):
        # extract input file name
        self.argParser.add_argument('-f', help="Input Filename", dest="filename", required = True)
        self.argParser.add_argument('-m', help="PDF mode", dest="mode", required = True)
        self.parserInitialized = True


    # triggers the whole pipeline of tasks
    def _allTasks(self):
        args = vars(self.argParser.parse_args())
        helper = FileHelper()
        fNameRaw = helper.GetFileName(args['filename'])
        # Step 0 - Create directories
        if not os.path.exists(self.parsedDataDir + fNameRaw + self.pathSeparator):
            os.makedirs(self.parsedDataDir + fNameRaw + self.pathSeparator)
        if not os.path.exists(self.reportDataDir + fNameRaw + self.pathSeparator):
            os.makedirs(self.reportDataDir + fNameRaw + self.pathSeparator)

        # Step 1 - Read PDF file
        #currentParser = TesseractParser.TesseractOcr(self.parsedDataDir + fNameRaw + self.pathSeparator)
        #currentParser.readFile(args['filename'], args['mode'])
        print("Step 1 - Done")

        # Step 2 - Clean up the file afterwards
        pdfFileRaw = self.parsedDataDir + fNameRaw + self.pathSeparator + fNameRaw  + ".plain"
        pdfFileClean = self.parsedDataDir + fNameRaw + self.pathSeparator + fNameRaw  + ".clean"
        cleaner = basic.Basic(self.parsedDataDir + fNameRaw + self.pathSeparator );
        cleaner.cleanUp(pdfFileRaw);
        print("Step 2 - Done")

        # Step 3 - Split it into dialog parts
        pdfFileDialog = self.parsedDataDir + fNameRaw + self.pathSeparator + fNameRaw  + ".dialog"
        with open(pdfFileClean, "r") as cleanFile:
            extractTool = extractor.Extractor(self.parsedDataDir + fNameRaw + self.pathSeparator , False)
            dialogParts = extractTool.Extract(cleanFile.read())
            extractTool.SaveToFile(dialogParts, pdfFileDialog)
        print("Step 3 - Done")

        # Step 4 - Split into sentences
        pdfFileSent = self.parsedDataDir + fNameRaw + self.pathSeparator + fNameRaw  + ".sentences"
        posTagger = textBlobPosTagger.TextBlobPosTagger()
        dialog = dialogContainer.Container()
        dialog.LoadFromFile(pdfFileDialog)
        dialogSent = dialogSentenceDialog.SentenceDialog(self.parsedDataDir + fNameRaw + self.pathSeparator, self.debug)
        dialogSent.SetDialog(dialog)
        dialogSent.SetPosTagger(posTagger)
        dialogSent.SplitTurnsToSentences()
        dialogSent.SaveToFile(fNameRaw+".sentences")
        print("Step 4 - Done")

        # Step 5 - Detect POS tags
        pdfFilePos = self.parsedDataDir + fNameRaw + self.pathSeparator + fNameRaw  + ".pos"
        posTagger = textBlobPosTagger.TextBlobPosTagger()
        dialogPos = dialogPosDialog.PosDialog(self.parsedDataDir + fNameRaw + self.pathSeparator, self.debug)
        dialogPos.SetDialogSent(dialogSent)
        dialogPos.SetPosTagger(posTagger)
        data = dialogPos.GetPosTaggedParts()
        dialogPos.SaveToFile(fNameRaw+".pos")
        print("Step 5 - Done")

        # Step 5 - Feature Extracct
        pdfFilePos = self.parsedDataDir + fNameRaw + self.pathSeparator + fNameRaw  + ".pos"
        posTagger = textBlobPosTagger.TextBlobPosTagger()
        dialogPos = dialogPosDialog.PosDialog(self.parsedDataDir + fNameRaw + self.pathSeparator, self.debug)
        dialogPos.SetDialogSent(dialogSent)
        dialogPos.SetPosTagger(posTagger)
        data = dialogPos.GetPosTaggedParts()
        dialogPos.SaveToFile(fNameRaw+".pos")
        print("Step 6 - Done")

        # Step 7 - Run Basic Reports
        self.__runBasicReports(dialog, fNameRaw)
        print("Step 7 - Done")

        # Step 8 - Run NLP Reports
        #self.__runNlpReports(dialogPos, dialog, fNameRaw)
        print("Step 8 - Done")


    # runs basic reports on the PDF
    def __runBasicReports(self, dialog, fNameRaw):
        report1 = turnsReport.Turns(self.reportDataDir + fNameRaw + self.pathSeparator )
        report1.SetDialog(dialog)
        data = report1.Turns()
        report1.SaveToFile(data)

        report2 = followReport.Follow(self.reportDataDir + fNameRaw + self.pathSeparator)
        report2.SetDialog(dialog)
        data = report2.Follows()
        report2.SaveToFile(data)

        report3 = followRatioReport.FollowRatio(self.reportDataDir + fNameRaw + self.pathSeparator)
        report3.SetDialog(dialog)
        #	report3.SetInterval(0.2, 0.5)
        data = report3.CalculateFollowRatio()
        report3.SaveToFile(data)

        report4 = mostFollowReport.MostFollow(self.reportDataDir + fNameRaw + self.pathSeparator)
        report4.SetDialog(dialog)
        report4.SetInterval(0.2, 0.7)
        data = report4.MostFollows()
        report4.SaveToFile(data)

        report5 = turnsPositionLengthReport.TurnsPositionLength(self.reportDataDir + fNameRaw + self.pathSeparator)
        report5.SetDialog(dialog)
        #		report5.SetInterval(0.2, 0.7)
        data = report5.AllTurns()
        report5.SaveToFile(data)

        report6 = mostWordsReport.MostWords(self.reportDataDir + fNameRaw + self.pathSeparator)
        report6.SetDialog(dialog)
        data = report6.CountWords()
        report6.SaveToFile(data)


    # runs NLP reports on the PDF
    def __runNlpReports(self, dialogPos, dialog, fNameRaw):
        helper = dialogHelper.Helper()
        people = helper.GetListPeople(dialogPos)

        report1 = nounPhrasePartsReport.NounPhraseParts(self.reportDataDir + fNameRaw + self.pathSeparator)
        report1.SetDialog(dialogPos)
        #    	nouns = report1.ExtractNounPhrases()

        report2 = usedNounsPersonReport.UsedNounsPerson(self.reportDataDir + fNameRaw + self.pathSeparator)
        report2.SetDialog(dialogPos)
        nouns = report2.FindUsedNounsRaw()
        report2.SaveToFile(nouns)

        report3 = topicChainIndexReport.TopicChainIndex(self.reportDataDir + fNameRaw + self.pathSeparator)
        report3.SetDialog(dialogPos)
        report3.SetThreshold(3)
        chains = report3.CalculateTci(nouns)
        report3.SaveToFile(chains)

        simProvider = wordnetLinSyns.Lin()
        simProvider.SetSimilarity(0.1)
        report4 = groupSynonymsTciReport.GroupSynonymsTci(self.reportDataDir + fNameRaw + self.pathSeparator)
        report4.SetDialog(dialogPos)
        report4.SetSimProvider(simProvider)
        grouppedChains = report4.GroupTci(chains)
        report4.SaveToFile(grouppedChains)
