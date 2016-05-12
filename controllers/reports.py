import controllers.base

# my tools
from tools.dialogs import container as dialogContainer
from tools.dialogs import posdialog as dialogPosDialog
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

class Reports(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'nlp-report' : self._nlpReports,
                                'report' : self._genericReports
        }


    # initializes its own parser
    def initializeArgumentParser(self):
        # extract input file name
        self.argParser.add_argument('-f', help="Filename", dest="filename", required=True)

        # extract optional output directory
        self.argParser.add_argument('-o', help="Optional output directory", dest="outputDir", default = None)
        self.parserInitialized = True


    # this part generates basic reports for the file
    def _genericReports(self):
        args = self.argParser.parse_args()
        fileName = args.filename
        if args.outputDir != None:
            self.reportDatadir = args.outputDir
    	dialog = dialogContainer.Container()
    	dialog.LoadFromFile(fileName)

    	report1 = turnsReport.Turns(self.reportDataDir)
    	report1.SetDialog(dialog)
    	data = report1.Turns()
    	if self.debug:
    		self.pprint.pprint("############ Report #1 - Most Turns")
    		self.pprint.pprint(data)
    	report1.SaveToFile(data)

        report2 = followReport.Follow(self.reportDataDir)
    	report2.SetDialog(dialog)
    	data = report2.Follows()
    	if self.debug:
    		self.pprint.pprint("")
    		self.pprint.pprint("")
    		self.pprint.pprint("############ Report #2 - Follows")
    		self.pprint.pprint(data)
    	report2.SaveToFile(data)

    	report3 = followRatioReport.FollowRatio(self.reportDataDir)
    	report3.SetDialog(dialog)
    #	report3.SetInterval(0.2, 0.5)
    	data = report3.CalculateFollowRatio()
    	if self.debug:
    		self.pprint.pprint("")
    		self.pprint.pprint("")
    		self.pprint.pprint("############ Report #3 - Follow Ratio")
    		self.pprint.pprint(data)
    	report3.SaveToFile(data)

        report4 = mostFollowReport.MostFollow(self.reportDataDir)
    	report4.SetDialog(dialog)
    	report4.SetInterval(0.2, 0.7)
    	data = report4.MostFollows()
    	if self.debug:
    		self.pprint.pprint("")
    		self.pprint.pprint("")
    		self.pprint.pprint("############ Report #4 - Most Follow")
    		self.pprint.pprint(data)
    	report4.SaveToFile(data)

    	report5 = turnsPositionLengthReport.TurnsPositionLength(self.reportDataDir)
    	report5.SetDialog(dialog)
    #		report5.SetInterval(0.2, 0.7)
    	data = report5.AllTurns()
    	if self.debug:
    		self.pprint.pprint("")
    		self.pprint.pprint("")
    		self.pprint.pprint("############ Report #5 - Turns with Position and Length")
    		self.pprint.pprint(data)
    	report5.SaveToFile(data)

        report6 = mostWordsReport.MostWords(self.reportDataDir)
        report6.SetDialog(dialog)
        data = report6.CountWords()
        if self.debug:
            self.pprint.pprint("")
            self.pprint.pprint("")
            self.pprint.pprint("############ Report #6 - Count Words per Person")
            self.pprint.pprint(data)
        report6.SaveToFile(data)


    # this part generates advanced reports rooted in NLP
    def _nlpReports(self):
        args = self.argParser.parse_args()
        fileName = args.filename
        if args.outputDir != None:
            self.reportDatadir = args.outputDir

        helper = dialogHelper.Helper()
    	dialogPos = dialogPosDialog.PosDialog(self.reportDataDir)
    	dialogPos.LoadFromFile(fileName)
        dialogPos.SetDialog( helper.AssignPositionsPartsDialog( dialogPos.GetDialog() ) )
#        self.__pprinter.pprint(dialogPos.GetDialog())
        people = helper.GetListPeople(dialogPos.GetDialog())

    	report1 = nounPhrasePartsReport.NounPhraseParts(self.reportDataDir)
    	report1.SetDialog(dialogPos)

#    	nouns = report1.ExtractNounPhrases()
    	if self.debug:
    		self.pprint.pprint("")
    		self.pprint.pprint("")
    		self.pprint.pprint("############ NLP Report #1 - Noun Phrases Parts")

    	report2 = usedNounsPersonReport.UsedNounsPerson(self.reportDataDir)
    	report2.SetDialog(dialogPos)

    	nouns = report2.FindUsedNounsRaw()
        if self.debug:
            self.pprint.pprint("")
            self.pprint.pprint("")
            self.pprint.pprint("############ NLP Report #2 - Used Nouns Per Person")
#            self.__pprinter.pprint(nouns)
        report2.SaveToFile(nouns)

        report3 = topicChainIndexReport.TopicChainIndex(self.reportDataDir)
    	report3.SetDialog(dialogPos)
        report3.SetThreshold(3)
        chains = report3.CalculateTci(nouns)
        if self.debug:
            self.pprint.pprint("")
            self.pprint.pprint("")
            self.pprint.pprint("############ NLP Report #3 - Topic Chain Index (treshold = 3)")
            self.__pprinter.pprint(chains)
        report3.SaveToFile(chains)

        simProvider = wordnetLinSyns.Lin()
        simProvider.SetSimilarity(0.1)
        report4 = groupSynonymsTciReport.GroupSynonymsTci(self.reportDataDir)
        report4.SetDialog(dialogPos)
        report4.SetSimProvider(simProvider)
        grouppedChains = report4.GroupTci(chains)
        if self.debug:
            self.pprint.pprint("")
            self.pprint.pprint("")
            self.pprint.pprint("############ NLP Report #4 - Group Topic Chain Index by person using synonyms")
            self.pprint.pprint(grouppedChains)
#        report4.SaveToFile(grouppedChains)
