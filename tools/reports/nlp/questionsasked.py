import csv

from tools.dialogs import person as personDialog
from tools.dialogs import helper as helperDialog
from tools.reports.nlp import nounphraseparts as nounPhrasePartsReport

# this class prepares reports from loaded dialog
# REPORT Description:
# The report returns list of questions asked by each person
class QuestionsAsked(object):

	# constructor
	def __init__(self, reportsDir):
		self._outputDir = reportsDir
		self._dialog_sentence = None


	# sets sentene dialog for this report
	def SetDialogSentence(self, newDialog):
		self._dialog_sentence = newDialog


	# returns list with used nouns per person (raw version not using WordNet)
	def FindAllQuestions(self, dfPositions):
		people = personDialog.Person()

		# prepare data structure
		result = {}

		# calculate
		currentPosition = ''
		for record in self._dialog_sentence.GetDialogSentences():
			key = '{}-{}-{}'.format(record['role'], record['name'], record['turn'])
			if key not in result:
				result[key] = people.GetEmptyQuestionPart(record['name'], record['role'])
				result[key]['turn'] = record['turn']
				if dfPositions[dfPositions['Turn'] == int(record['turn'])].shape[0] > 0:
					currentPosition = dfPositions[dfPositions['Turn'] == int(record['turn'])]['Position'].values[0]
				result[key]['position'] = currentPosition

			if '?' in record['sentence']:
				result[key]['count'] += 1
		return result


	# this method saveds data produced by this report to a CSV file
	def SaveToFile(self, data, name = None):
		fileName = 'questions_asked.csv'
		if name != None:
			fileName = name + ".csv"

		list_results = sorted([(data[key]['role'], data[key]['name'], int(data[key]['turn']), data[key]['count'], data[key]['position']) for key in data.keys()], key=lambda x:x[2])

		with open(self._outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(['Role', 'Name', 'Turn', 'Count', 'Position'])
			for record in list_results:
				writer.writerow(record)
