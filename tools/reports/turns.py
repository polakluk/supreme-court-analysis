import csv
from tools.dialogs import person as personDialog
from tools.dialogs import helper as dialogHelper

# this class prepares reports from loaded dialog
# it expect list of Person objects
# REPORT Description:
# The report counts the longest chain of question asked by each justice
class Turns:

	# constructor
	def __init__(self, reportsDir):
		self.__outputDir = reportsDir
		self.__dialog = None


	# sets dialog for this report
	def SetDialog(self, newDialog):
		self.__dialog = newDialog


	# calculates longest turns per each justice
	def Turns(self):
		if self.__dialog == None:
			return None

		helper = dialogHelper.Helper()

		peopleHandler = personDialog.Person()
		people = helper.GetListPeople(self.__dialog.GetDialog(), True)

		res = {}
		# prepare data structure
		for personItem in people:
			res['|'.join(personItem)] = 0

		# walk through the dialog and calculate it
		previousPerson = None
		actCounter = 1
		for part in self.__dialog.GetDialog():
			# the report is only intersted in exchange between justices
			if part['role'] == 'other':
				continue

			actPerson = part['role']+ "|" + part['name']
			if actPerson == previousPerson or previousPerson == None:
				# the chain continues
				actCounter += 1
			else:
				# the chain of talks jus broke, so keep track of this, if you need to
				if res[previousPerson] < actCounter:
					res[previousPerson] = actCounter

				actCounter = 1 # reset counter

			previousPerson = actPerson

		# convert the results back into list of Person objects
		resKeys = res.keys()
		final = sorted([peopleHandler.GetEmptyReportTurns( key.split('|'), res[key] ) for key in resKeys],
						 key = lambda x: x['turns'], reverse = True)
		return final


	# this method saveds data produced by this report to a CSV file
	def SaveToFile(self, data, name = None):
		fileName = 'turns.csv'
		if name != None:
			fileName = name + ".csv"

		with open(self.__outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(['Role', 'Name', 'Turns'])
			for row in data:
				writer.writerow([row['role'], row['name'], row['turns']])
