import pandas as pd
import csv
from tools.dialogs import person as personDialog
from tools.filehelper import FileHelper


# This class takes care of POS tagging whole dialog, saving the tags and loading it
class PosDialog(object):

	# constructor
	def __init__(self, parsedDir, isDebug = False):
		self.__outputDir = parsedDir
		self.__dialogSent = None
		self.__list_parts_pos = None
		self.__pos_tagger = None
		self.__word_delimiter = '^^^'
		self.__pos_delimiter = '||'
		self.__isDebug = isDebug


	# sets POS tagger
	def SetPosTagger(self, newPos):
		self.__pos_tagger = newPos


	# sets dialog for this report
	def SetDialogSent(self, newDialog):
		self.__dialogSent = newDialog


	# returns dialog with POS tags
	def GetDialogPos(self):
		return self.__list_parts_pos


	# runs associated POS tagger on the dialog
	def GetPosTaggedParts(self, refresh = False):
		if self.__pos_tagger == None and self.__list_parts_pos == None:
			return None

		if self.__list_parts_pos == None or refresh:
			self.__list_parts_pos = []
			parts = self.__dialogSent.GetDialogSentences()
			people = personDialog.Person()

			for part in parts:
				obj = people.GetEmptyPosPerson(part['name'], part['turn'], part['sentence'], part['sentence_id'],
												part['was_interrupted'], part['role'])
				obj['pos'] = self.__pos_tagger.Tag( part['sentence'], self.__isDebug)
				self.__list_parts_pos.append(obj)

		return self.__list_parts_pos


	# save files to a CSV file
	def SaveToFile(self, name = None):
		helper = FileHelper()
		fileName = helper.GetFileName(name) + ".pos"

		with open( self.__outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(['Turn', 'Sentence ID', 'Sentence', 'POS', 'Role', 'Name', 'Was Interrupted'])
			for part in self.__list_parts_pos:
				was_interrupted = '0'
				if part['was_interrupted']:
					was_interrupted = '1'
				pos_arr = self.__word_delimiter.join([ word[0]+self.__pos_delimiter+word[1] for word in part['pos'] ])
				writer.writerow([part['turn'], part['sentence_id'], part['sentence'],
								pos_arr, part['role'], part['name'], was_interrupted])


	# load POS tags from file
	def LoadFromFile(self, fName):
		self.__list_parts_pos = []
		self.__dialog = []
		people = personDialog.Person()
		with open(fName, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			skippedFirstLine = False
			for row in reader:
				# skip header line
				if skippedFirstLine:
					obj = people.GetEmptyPosPerson(row[5], row[0], row[2], row[1], row[6] == '1', row[4])

					# parse words and sentences
					sentences = [word.split(self.__pos_delimiter) for word in row[3].split(self.__word_delimiter)]
					obj['pos'] = sentences
					self.__list_parts_pos.append(obj)
				else:
					skippedFirstLine = True



	# returns the dialog with POS tags as dataframe
	def AsDataFrame(self):
		if self.__list_parts_pos is None:
			return pd.DataFrame({})

		data = []
		for part in self.__list_parts_pos:
			line = [part['name'], part['role'], part['turn'], part['sentence'], part['sentence_id'],
					part['pos'], part['was_interrupted']]
			data.append(line)

		return pd.DataFrame(data, columns = ['name', 'role', 'turn', 'sentence', 'sentence_id', 'pos', 'was_interrupted'])
