import csv

from tools.dialogs import person as personDialog
from tools.filehelper import FileHelper


# This class takes care of splitting turns into sentences, saving the them and loading them
class SentenceDialog(object):

	# constructor
	def __init__(self, parsedDir, isDebug = False):
		self._outputDir = parsedDir
		self._dialog = None
		self._list_parts_sentences = None
		self._pos_tagger = None
		self._isDebug = isDebug


	# sets POS tagger
	def SetPosTagger(self, newPos):
		self._pos_tagger = newPos


	# sets dialog for this report
	def SetDialog(self, newDialog):
		self._dialog = newDialog


	# returns only dialog
	def GetDialog(self):
		return self._dialog


	# returns dialog sentences
	def GetDialogSentences(self):
		return self._list_parts_sentences


	# this method splits turns to sentences so sentiment analysis can be run
	def SplitTurnsToSentences(self):
		if self._pos_tagger == None and self._list_parts_sentences == None:
			return None

		if self._list_parts_sentences == None or refresh:
			self._list_parts_sentences = []
			parts = self.__dialog.GetDialog()
			people = personDialog.Person()
			idx = 0

			for part in parts:
				sentences = self._pos_tagger.SeparateSentenctes(part['text'])
				sent_id = 0
				for sent in sentences:
					obj = people.GetEmptySentencePerson(part['name'], idx, sent, sent_id, part['was_interrupted'], part['role'])
					self._list_parts_sentences.append(obj)
					sent_id += 1

				idx += 1


		return self._list_parts_sentences


	# save files to a CSV file
	def SaveToFile(self, name = None):
		helper = FileHelper()
		fileName = helper.GetFileName(name) + ".sentences"

		with open( self._outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(['Turn', 'Sentence ID', 'Sentence', 'Role', 'Name', 'Was Interrupted'])
			for part in self._list_parts_sentences:
				was_interrupted = '0'
				if part['was_interrupted']:
					was_interrupted = '1'

				writer.writerow([part['turn'], part['sentence_id'], part['sentence'], part['role'], part['name'], was_interrupted])


	# load sentences from file
	def LoadFromFile(self, fName):
		self._list_parts_sentences = []
		people = personDialog.Person()
		with open(fName, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			skippedFirstLine = False
			for row in reader:
				# skip header line
				if skippedFirstLine:
					obj = people.GetEmptySentencePerson(row[4], row[0], row[2], row[1], row[5] == '1', row[3])
					self._list_parts_sentences.append(obj)
				else:
					skippedFirstLine = True
