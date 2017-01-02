from tools.dialogs import person as personDialog
import numpy as np


# this class prepares reports from loaded dialog
# REPORT Description:
# The report returns list of noun-related words in each sentence per dialog part
# NOTE:
# This report is not meant to be saved
class NounPhraseParts(object):

	# constructor
	def __init__(self, reportsDir):
		self.__outputDir = reportsDir
		self._dialog = None
		self._dialog_pos = None
		self._noun_tags = ['NN', 'NNP', 'NNS']


	# sets dialog for this report
	def SetDialog(self, newDialog):
		self._dialog = newDialog


	# sets POS dialog for this report
	def SetDialogPos(self, newDialog):
		self._dialog_pos = newDialog


	# returns list with noun phrases
	def ExtractNounPhrases(self):
		people = personDialog.Person()
		# dont do anything unless everything is properly set up
		parts = self._dialog_pos.GetDialogPos()
		if parts == None:
			return None

		result = []
		for part in parts:
			uniqueNouns = set()
			if len(part['sentence']) < 2:
				continue
			[ uniqueNouns.add(w[0].lower()) for w in part['pos'] if (w[1] in self._noun_tags) and len(w[0]) > 1]
			result.append(people.GetEmptyNounsPerson(part['name'], part['role'], uniqueNouns))
		return result


	# saves the report to file
	def SaveToFile(self):
		return None