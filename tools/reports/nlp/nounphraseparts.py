from tools.dialogs import person as personDialog

# this class prepares reports from loaded dialog
# REPORT Description:
# The report returns list of noun-related words in each sentence per dialog part
class NounPhraseParts:

	# constructor
	def __init__(self, reportsDir):
		self.__outputDir = reportsDir
		self.__dialog = None


	# sets dialog for this report
	def SetDialog(self, newDialog):
		self.__dialog = newDialog


	# returns list with noun phrases
	def ExtractNounPhrases(self):
		people = personDialog.Person()
		# dont do anything unless everything is properly set up
		parts = self.__dialog.GetDialogPos()
		if parts == None:
			return None

		result = []
		for part in parts:
			nounphrase = [ [w for w in sentence if w[1][0] == 'N'] for sentence in part['pos']]
			result.append(people.GetEmptyNounsPerson(part['name'], part['role'], nounphrase))
		return result


	# saves the report to file
	def SaveToFile(self):
		return None
