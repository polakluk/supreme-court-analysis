import csv
from nltk.corpus import stopwords

from tools.dialogs import person as personDialog
from tools.dialogs import helper as helperDialog
from tools.reports.nlp import nounphraseparts as nounPhrasePartsReport

# this class prepares reports from loaded dialog
# REPORT Description:
# The report returns list of used nouns per person with their respective counts. For more accurate results taking synonyms into account, it uses synonyms provider
class UsedNounsPerson:

	# constructor
	def __init__(self, reportsDir):
		self.__outputDir = reportsDir
		self.__dialog = None
		self.__nounPhrases = None
		self.__synonymsProvider = None
		self.__synonymSimilarity = 0.5
		self.__stopwords = stopwords.words('english')


	# sets dialog for this report
	def SetDialog(self, newDialog):
		self.__dialog = newDialog


	# sets synonyms provider for this report
	def SetSynonymsProvider(self, provider):
		self.__synonymsProvider = provider


	def SetSynonymSimilarity(self, similarity):
		self.__synonymSimilarity = similarity


	# loads noun phrases and caches them in array
	def LoadNounPhrases(self):
		report = nounPhrasePartsReport.NounPhraseParts(self.__outputDir)
		report.SetDialog(self.__dialog)
		self.__nounPhrases = report.ExtractNounPhrases()


	# returns list with used nouns per person (raw version not using WordNet)
	def FindUsedNounsRaw(self):
		people = personDialog.Person()
		# dont do anything unless everything is properly set up
		# check, if noun phrases were loaded
		if self.__nounPhrases == None:
			self.LoadNounPhrases()

		# check the noun phrases one more time - if they arent loaded up, then there arent any
		if self.__nounPhrases == None:
			return None

		# prepare data structure
		helper = helperDialog.Helper()
		listPeople = helper.GetListPeople(self.__dialog.GetDialog())
		result = {}
		for person in listPeople:
			result[person[1]] = people.GetEmptyNounsPerson(person[1], person[0], {})

		for phrase in self.__nounPhrases:
			for word in phrase['nouns']:
				if word in self.__stopwords: # skip stopwords
					continue

				if word in result[phrase['name']]['nouns'].keys():
					result[phrase['name']]['nouns'][word] += 1
				else:
					result[phrase['name']]['nouns'][word] = 1

		# sort results for each person
		for key in result.keys():
			if len(result[key]['nouns'].keys()):
				# first, conert it to list of tuples
				result[key]['nouns'] = [(noun, result[key]['nouns'][noun]) for noun in result[key]['nouns'].keys()]
				result[key]['nouns'].sort(key = lambda x: x[1], reverse = True)
			else:
				result[key]['nouns'] = []

		return result


	# this method saveds data produced by this report to a CSV file
	def SaveToFile(self, data, name = None):
		fileName = 'usednouns.csv'
		if name != None:
			fileName = name + ".csv"

		with open(self.__outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(['Role', 'Name', 'Noun', 'Count'])
			for idx in data.keys():
				row = data[idx]
				if len(row['nouns']):
					for nounTuple in row['nouns']:
						writer.writerow([row['role'], row['name'], nounTuple[0], nounTuple[1]])
