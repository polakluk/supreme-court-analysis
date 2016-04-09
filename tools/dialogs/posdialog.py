import csv
from tools.dialogs import person as personDialog
from tools.filehelper import FileHelper


# This class takes care of POS tagging whole dialog, saving the tags and loading it
class PosDialog:

	# constructor
	def __init__(self, parsedDir, isDebug = False):
		self.__outputDir = parsedDir
		self.__dialog = None
		self.__list_parts_pos = None
		self.__pos_tagger = None
		self.__sentence_delimiter = '###'
		self.__word_delimiter = '^^^'
		self.__pos_delimiter = '||'
		self.__isDebug = isDebug


	# sets POS tagger
	def SetPosTagger(self, newPos):
		self.__pos_tagger = newPos


	# sets dialog for this report
	def SetDialog(self, newDialog):
		self.__dialog = newDialog
		self.__list_parts_pos = None


	# returns only dialog
	def GetDialog(self):
		return self.__dialog


	# returns dialog with POS tags
	def GetDialogPos(self):
		return self.__list_parts_pos


	# runs associated POS tagger on the dialog
	def GetPosTaggedParts(self, refresh = False):
		if self.__pos_tagger == None and self.__list_parts_pos == None:
			return None

		if self.__list_parts_pos == None or refresh:
			self.__list_parts_pos = []
			parts = self.__dialog.GetDialog()
			people = personDialog.Person()
			idx = 0

			for part in parts:
				if self.__isDebug:
					print("Start tagging "+str(idx))
				obj = people.GetEmptyPosPerson(part['name'], part['text'], part['was_interrupted'], part['role'])
				obj['pos'] = self.__pos_tagger.Tag( self.__pos_tagger.SeparateSentenctes(part['text']), self.__isDebug)
				self.__list_parts_pos.append(obj)

				if self.__isDebug:
					print("End tagging "+str(idx))

				idx += 1


		return self.__list_parts_pos


	# save files to a CSV file
	def SaveToFile(self, name = None):
		helper = FileHelper()
		fileName = helper.GetFileName(name) + ".pos"

		with open( self.__outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(['Role', 'Name', 'Text', 'Was Interrupted', 'POS'])
			for part in self.__list_parts_pos:
				was_interrupted = '0'
				if part['was_interrupted']:
					was_interrupted = '1'



				pos_arr = [self.__word_delimiter.join([ word[0]+self.__pos_delimiter+word[1] for word in sentence ]) for sentence in part['pos']]

				writer.writerow([part['role'], part['name'], part['text'], was_interrupted, self.__sentence_delimiter.join(pos_arr)])


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
					obj = people.GetEmptyPosPerson(row[1], row[2], row[3] == '1', row[0])

					# parse words and sentences
					sentences = [[word.split(self.__pos_delimiter) for word in sentence.split(self.__word_delimiter)] for sentence in row[4].split(self.__sentence_delimiter)]
					obj['pos'] = sentences
					self.__list_parts_pos.append(obj)

					# maintain original Dialog object too
					objOriginal = people.GetEmpty()
					objOriginal['role'] = row[0]
					objOriginal['name'] = row[1]
					objOriginal['text'] = row[2]
					objOriginal['was_interrupted'] = row[3] == '1'
					self.__dialog.append(objOriginal);

				else:
					skippedFirstLine = True