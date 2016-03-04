from tools.dialogs import person as personDialog
from tools.reports import follow as followReport

# this class prepares reports from loaded dialog
# it expect list of Person objects
# REPORT Description:
# The report returns list of pair of justices. The first part contains name of justice.
# The second part contains name of justice who follows them  
class MostFollow:

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

	# returns the list of pair of justices 
	def MostFollows(self):
		if self.__dialog == None:
			return []

		peopleHandler = personDialog.Person()
		people = self.__dialog.GetListPeople() 
		
		res = {}
		# prepare data structure
		for personItem in people:
			res['|'.join(personItem)] = 0

		report = followReport.Follow(self.__outputDir)
		report.SetDialog(self.__dialog)
		follows = report.Follows()

		# filter only interesting part for this report, if needed
		if self.__interval_start != 0 or self.__interval_end != 1.0:
			follows = [p for p in follows if p['values']['position'] >= self.__interval_start and  p['values']['position'] <= self.__interval_end]

		if len(follows) == 0:
			return res
		return res
