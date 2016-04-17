from tools.dialogs import person as personDialog
from tools.dialogs import helper as helperDialog
from tools.reports.nlp import topicchainindex as topicChainIndexReport
from tools.reports.nlp import usednounsperson as usedNounsPersonReport


# this class prepares reports from loaded dialog
# REPORT Description:
# The report returns list of nouns grouped by synonyms.
# Under the hood, it takes TCI for each person and concats them
# The report still does this operation for each person separately
class GroupSynonymsTci:

	# constructor
	def __init__(self, reportsDir):
		self.__outputDir = reportsDir
		self.__dialog = None
		self.__synProvider = None


	# sets dialog for this report
	def SetDialog(self, newDialog):
		self.__dialog = newDialog


	# sets synonyms provider
	def SetSynProvider(self, provider):
		self.__synProvider = provider


	# returns list with noun phrases
	def GroupTciByPerson(self):
		people = personDialog.Person()
		# dont do anything unless everything is properly set up
		parts = self.__dialog.GetDialogPos()
		if parts == None:
			return None

		helper = helperDialog.Helper()
		listPeople = helper.GetListPeople(self.__dialog.GetDialog())
		result = []
		# first, extract nouns
		report1 = usedNounsPersonReport.UsedNounsPerson(self.__outputDir)
		report1.SetDialog(self.__dialog)
		nouns = report1.FindUsedNounsRaw()

		report2 = topicChainIndexReport.TopicChainIndex(self.__outputDir)
		report2.SetDialog(self.__dialog)

		chains = []
		for person in listPeople:
			for noun in nouns[person[1]]['nouns']:
				chains[person[1]+'|'+person[0]+"|" + noun] = report2.CalculateTciPerson(person[1], person[0], [[noun]])

		return result


	# saves the report to file
	def SaveToFile(self, data):
		return None
