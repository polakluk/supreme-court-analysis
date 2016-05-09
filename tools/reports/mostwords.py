import csv
from nltk import word_tokenize

from tools.dialogs import person as personDialog
from tools.dialogs import helper as dialogHelper

# this class prepares reports from loaded dialog
# it expect list of Person objects
# REPORT Description:
# The report counts the number of words per person
class MostWords(object):

	# constructor
	def __init__(self, reportsDir):
		self.__outputDir = reportsDir
		self.__dialog = None


	# sets dialog for this report
	def SetDialog(self, newDialog):
		self.__dialog = newDialog


	# calculates longest turns per each justice
	def CountWords(self):
		if self.__dialog == None:
			return None

		helper = dialogHelper.Helper()

		peopleHandler = personDialog.Person()
		people = helper.GetListPeople(self.__dialog.GetDialog())

		res = {}
		# prepare data structure
		for personItem in people:
			res['|'.join(personItem)] = peopleHandler.GetEmptyCountWordsPerson(personItem[1], personItem[0], 0, 0, 0)

		# walk through the dialog and calculate it
		for part in self.__dialog.GetDialog():
			actPerson = part['role']+ "|" + part['name']
			words = word_tokenize(part['text'])
			res[actPerson]['words'] += len(words)
			res[actPerson]['turns'] += 1

		for idx in res.keys():
			res[idx]['wordsPerTurn'] = float(res[idx]['words']) / res[idx]['turns']

		# sort the final list by most words
		res = sorted(res.values(), key = lambda x: x['words'], reverse = True)
		return res


	# this method saveds data produced by this report to a CSV file
	def SaveToFile(self, data, name = None):
		fileName = 'words.csv'
		if name != None:
			fileName = name + ".csv"

		with open(self.__outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(['Role', 'Name', 'Words', 'Turns', 'Words per Turn'])
			for row in data:
				writer.writerow([row['role'], row['name'], row['words'], row['turns'], row['wordsPerTurn']])
