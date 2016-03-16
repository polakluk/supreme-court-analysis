

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
		# dont do anything unless everything is properly set up
		if self.__dialog == None or self.__pos_tagger == None:
			return None

		parts = self.__dialog.GetDialog()

		return []


	# applies POS tagger to a part of dialog
	def __applyPosTagger(self, text):
		return []


	# saves the report to file
	def SaveToFile(self):
		return None