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
        super(basecontroller.Base, self).__init__(pprinter, argParse)
        self.availableTask = {
                                'nlp-report' : self._nlpReports,
                                'report' : self._genericReports
        }

    # this part generates basic reports for the file
    def _generateReports(self, fileName):
    	dialog = dialogContainer.Container()
    	dialog.LoadFromFile(fileName)

    	report1 = turnsReport.Turns(self.__reportDatadir)
    	report1.SetDialog(dialog)
    	data = report1.Turns()
    	if self.__isDebug:
    		print("############ Report #1 - Most Turns")
    		self.__pprinter.pprint(data)
    	report1.SaveToFile(data)

    	report2 = followReport.Follow(self.__reportDatadir)
    	report2.SetDialog(dialog)
    	data = report2.Follows()
    	if self.__isDebug:
    		print
    		print
    		print("############ Report #2 - Follows")
    		self.__pprinter.pprint(data)
    	report2.SaveToFile(data)

    	report3 = followRatioReport.FollowRatio(self.__reportDatadir)
    	report3.SetDialog(dialog)
    #	report3.SetInterval(0.2, 0.5)
    	data = report3.CalculateFollowRatio()
    	if self.__isDebug:
    		print
    		print
    		print("############ Report #3 - Follow Ratio")
    		self.__pprinter.pprint(data)
    	report3.SaveToFile(data)

    	report4 = mostFollowReport.MostFollow(self.__reportDatadir)
    	report4.SetDialog(dialog)
    	report4.SetInterval(0.2, 0.7)
    	data = report4.MostFollows()
    	if self.__isDebug:
    		print
    		print
    		print("############ Report #4 - Most Follow")
    		self.__pprinter.pprint(data)
    	report4.SaveToFile(data)

    	report5 = turnsPositionLengthReport.TurnsPositionLength(self.__reportDatadir)
    	report5.SetDialog(dialog)
    #		report5.SetInterval(0.2, 0.7)
    	data = report5.AllTurns()
    	if self.__isDebug:
    		print
    		print
    		print("############ Report #5 - Turns with Position and Length")
    		self.__pprinter.pprint(data)
    	report5.SaveToFile(data)

        report6 = mostWordsReport.MostWords(self.__reportDatadir)
        report6.SetDialog(dialog)
        data = report6.CountWords()
        if self.__isDebug:
            print
            print
            print("############ Report #6 - Count Words per Person")
            self.__pprinter.pprint(data)
        report6.SaveToFile(data)


    # this part generates advanced reports rooted in NLP
    def _nlpReports(self, fileName):
        helper = dialogHelper.Helper()
    	dialogPos = dialogPosDialog.PosDialog(self.__reportDatadir)
    	dialogPos.LoadFromFile(fileName)
        dialogPos.SetDialog( helper.AssignPositionsPartsDialog( dialogPos.GetDialog() ) )
#        self.__pprinter.pprint(dialogPos.GetDialog())
        people = helper.GetListPeople(dialogPos.GetDialog())

    	report1 = nounPhrasePartsReport.NounPhraseParts(self.__reportDatadir)
    	report1.SetDialog(dialogPos)

#    	nouns = report1.ExtractNounPhrases()
    	if self.__isDebug:
    		print
    		print
    		print("############ NLP Report #1 - Noun Phrases Parts")

    	report2 = usedNounsPersonReport.UsedNounsPerson(self.__reportDatadir)
    	report2.SetDialog(dialogPos)

    	nouns = report2.FindUsedNounsRaw()
        if self.__isDebug:
            print
            print
            print("############ NLP Report #2 - Used Nouns Per Person")
#            self.__pprinter.pprint(nouns)
        report2.SaveToFile(nouns)


        report3 = topicChainIndexReport.TopicChainIndex(self.__reportDatadir)
    	report3.SetDialog(dialogPos)
        report3.SetThreshold(3)
        chains = report3.CalculateTci(nouns)
        if self.__isDebug:
            print
            print
            print("############ NLP Report #3 - Topic Chain Index (treshold = 3)")
            self.__pprinter.pprint(chains)
        report3.SaveToFile(chains)

        simProvider = wordnetLinSyns.Lin()
        simProvider.SetSimilarity(0.1)
        report4 = groupSynonymsTciReport.GroupSynonymsTci(self.__reportDatadir)
        report4.SetDialog(dialogPos)
        report4.SetSimProvider(simProvider)
        grouppedChains = report4.GroupTci(chains)
        if self.__isDebug:
            print
            print
            print("############ NLP Report #4 - Group Topic Chain Index by person using synonyms")
            self.__pprinter.pprint(grouppedChains)
#        report4.SaveToFile(grouppedChains)
