from tools.dialogs import person as personDialog
from tools.dialogs import helper as dialogHelper
from tools.reports import followratio as followRatioReport

import csv

# this class prepares reports from loaded dialog
# it expect list of Person objects
# REPORT Description:
# The report returns list of pair of justices. The first part contains name of justice.
# The second part contains name of justice who follows them
class MostFollow(object):

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
			return None

		helper = dialogHelper.Helper()
		# prepare data structures
		peopleHelper = personDialog.Person()
		people = helper.GetListPeople(self.__dialog.GetDialog(), True)
		res = {}

		# get data about followe ratio for eah justice
		report = followRatioReport.FollowRatio(self.__outputDir)
		report.SetDialog(self.__dialog)
		report.SetInterval(self.__interval_start, self.__interval_end)
		ratios = report.CalculateFollowRatio()

		if ratios == None: # no information for selected interal
			return None

		# extract the most followed-after justice per each justice
		resKeys = ratios.keys()
		for key in resKeys:
			followKeys = ratios[key].keys()
			bestKey = None
			for keyFollow in followKeys:
				if keyFollow == '__num':
					continue
				if bestKey == None or ratios[key][bestKey] < ratios[key][keyFollow]:
					if float(ratios[key][keyFollow]) > 0.001:
						bestKey = keyFollow

			if bestKey == None:
				res[key] = peopleHelper.GetEmptyReportMostFollow( key.split('|'),
																0.0,
																None)
			else:
				res[key] = peopleHelper.GetEmptyReportMostFollow( key.split('|'),
																ratios[key][bestKey],
																bestKey)

		return res


	# this method saveds data produced by this report to a CSV file
	def SaveToFile(self, data, name = None):
		fileName = 'mostfollow.csv'
		if name != None:
			fileName = name + ".csv"

		with open(self.__outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(['Role', 'Name', 'Follower Role', 'Follower Name', 'Ratio'])
			dataKeys = data.keys()
			for key in dataKeys:
				follower = ['---', '---']
				if data[key]['follower'] != None:
					follower = data[key]['follower'].split('|')
				writer.writerow([data[key]['role'], data[key]['name'], follower[0], follower[1], data[key]['ratio']])
