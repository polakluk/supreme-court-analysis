from tools.reports.nlp import nounphraseparts as nounPhrasePartsReport

# this class prepares reports from loaded dialog
# it expect list of Person objects
# REPORT Description:
# The report returns list of noun phrases extracted from each part of dialog
class NounPhrases:

	# constructor
	def __init__(self, reportsDir):
		self.__outputDir = reportsDir
		self.__dialog = None
		self.__interval_start = 0.0
		self.__interval_end = 1.0


	# sets dialog for this report
	def SetDialog(self, newDialog):
		self.__dialog = newDialog


	# sets interval of interest for this report
	def SetInterval(self, start, end):
		self.__interval_start = start
		self.__interval_end = end


	# returns list with noun phrases
	def ExtractNounPhrases(self):
		report = nounPhrasePartsReport()
		report.SetDialog(self.__dialog)
		parts = report.ExtractNounPhrases()

		# dont do anything unless everything is properly set up
		if parts == None:
			return None

		result = []

		return result


	# applies POS tagger to a part of dialog
	def __applyPosTagger(self, text):
		return []


	# saves the report to file
	def SaveToFile(self):
		return None
