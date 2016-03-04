from tools.dialogs import person as personDialog
from tools.reports import follow as followReport

# this class prepares reports from loaded dialog
# it expect list of Person objects
# REPORT Description:
# The report returns dictionary of justices. For each item in dictionary, it returns a dictionary
# containing names of all other justices and ratio, how often they follow the justice
class FollowRatio:

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
	def CalculateFollowRatio(self):
		if self.__dialog == None:
			return []

		peopleHandler = personDialog.Person()
		people = self.__dialog.GetListPeople() 
		
		report = followReport.Follow(self.__outputDir)
		report.SetDialog(self.__dialog)
		follows = report.Follows()

		res = {}
		# prepare data structure
		for personItem in people:
			numFollows = len([item for item in follows if item['name'] == personItem[1] and item['role'] == personItem[0]])
			res['|'.join(personItem)] = self.__prepareDictionary(personItem[1], numFollows )


		# filter only interesting part for this report, if needed
		if self.__interval_start != 0 or self.__interval_end != 1.0:
			follows = [p for p in follows if p['values']['position'] >= self.__interval_start and  p['values']['position'] <= self.__interval_end]

		# are there any follows to analyze?
		if len(follows) == 0:
			return res

		# there are, so let's get our hands dirty
		for item in follows:
			actPerson = item['role'] + "|" + item['name']
			res[actPerson][item['follower']] += 1


		print(res)
		return res


	# prepares dictionary for each justice with all justices skipping record for the justice themselves
	# the dictionary containts item __num represents total number of follows for this judge
	def __prepareDictionary(self, skip, num):
		people = self.__dialog.GetListPeople()

		res = {'__num' : num }
		# prepare data structure
		for personItem in people:
			if personItem[1] == skip: # skip the justice himself
				res['|'.join(personItem)] = 0.0

		return res
