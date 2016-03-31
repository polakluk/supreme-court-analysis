import csv
from tools.dialogs import person as personDialog
from tools.dialogs import helper as dialogHelper

# this class prepares reports from loaded dialog
# it expect list of Person objects
# REPORT Description:
# The report counts turns per person in dialog and stores their position and length
class TurnsPositionLength:

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


	# calculates all turns, their length and position in dialog
	def AllTurns(self):
		if self.__dialog == None:
			return None

		helper = dialogHelper.Helper()
		peopleHandler = personDialog.Person()
		res = []

		# walk through the dialog and calculate it
		previousPerson = None
		actCounter = 0
		actJusticePart = 0
		numPartsJustices = float(helper.CountJusticesParts(self.__dialog.GetDialog()))
		for part in self.__dialog.GetDialog():
			# the report is only intersted in exchange between justices
			if part['role'] == 'other':
				continue

			actPerson = part['role']+ "|" + part['name']
			if actPerson == previousPerson or previousPerson == None:
				# the chain continues
				actCounter += 1
			else:
				# another turn start right about now, so save this one
				pos = actJusticePart / numPartsJustices
				length = actCounter
				infoQuality = actCounter / numPartsJustices
				res.append(peopleHandler.GetEmptyReportTurnLength(actPerson.split('|'), pos, length, infoQuality))

				actJusticePart += actCounter
				actCounter = 1 # reset counter


			previousPerson = actPerson

		# filter only interesting part for this report, if needed
		if self.__interval_start != 0 or self.__interval_end != 1.0:
			res = [p for p in res if p['position'] >= self.__interval_start and
											p['position'] <= self.__interval_end]

		return res


	# this method saveds data produced by this report to a CSV file
	def SaveToFile(self, data, name = None):
		fileName = 'allturns.csv'
		if name != None:
			fileName = name + ".csv"

		with open(self.__outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(['Role', 'Name', 'Length', 'Position', 'Information'])
			for row in data:
				writer.writerow([row['role'], row['name'], row['length'], row['position'], row['information']])
