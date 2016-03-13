import csv

from tools.dialogs import person as personDialog

# this class prepares reports from loaded dialog
# it expect list of Person objects
# REPORT Description:
# The report returns list of followers of justices. The first part contains name of justice.
# The second part contains name of justice who follows them.
# The third part represents position in dialog, when the exchange occured  
class Follow:

	# constructor
	def __init__(self, reportsDir):
		self.__outputDir = reportsDir
		self.__dialog = None


	# sets dialog for this report
	def SetDialog(self, newDialog):
		self.__dialog = newDialog


	# returns the list of pair of justices 
	def Follows(self):
		peopleHandler = personDialog.Person()
		res = []

		# walk through the dialog and calculate it
		previousPerson = None
		actJusticePart = 0
		numPartsJustices = float(self.__dialog.CountJusticesParts())
		for part in self.__dialog.GetDialog():
			# the report is only intersted in exchange between justices
			if part['role'] == 'other':
				continue

			actJusticePart += 1
			actPerson = part['role'] + "|" + part['name']
			# remember this exchange
			if previousPerson != None and previousPerson != actPerson:
				# this person follows somebody
				position = actJusticePart / numPartsJustices
				res.append(peopleHandler.GetEmptyReportFollows( actPerson.split('|'), 
																previousPerson,
																position ))

			previousPerson = actPerson


		return res


	# this method saveds data produced by this report to a CSV file
	def SaveToFile(self, data, name = None):
		fileName = 'follow.csv'
		if name != None:
			fileName = name + ".csv"

		with open(self.__outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(['Role', 'Name', 'Followee Role', 'Followee Name', 'Position'])
			for row in data:
				follower = row['followee'].split('|')
				writer.writerow([row['role'], row['name'], follower[0], follower[1], str(row['position'])])
