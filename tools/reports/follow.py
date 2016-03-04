from operator import attrgetter

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
																part['name'], previousPerson.split('|')[1],
																position ))

			previousPerson = actPerson


		return res
