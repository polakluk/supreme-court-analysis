import csv
from nltk.corpus import stopwords

from tools.dialogs import person as personDialog
from tools.dialogs import helper as helperDialog
from tools.reports.nlp import nounphraseparts as nounPhrasePartsReport

# this class prepares reports from loaded dialog
# REPORT Description:
# The report returns list of used nouns per person with their respective counts. For more accurate results taking synonyms into account, it uses synonyms provider
class UsedNounsPerson(object):

	# constructor
	def __init__(self, reportsDir):
		self._outputDir = reportsDir
		self._dialog = None
		self._dialog_pos = None
		self._nounPhrases = None
		self._synonymsProvider = None
		self._stopwords = stopwords.words('english')


	# sets dialog for this report
	def SetDialog(self, newDialog):
		self._dialog = newDialog


	# sets POS dialog for this report
	def SetDialogPos(self, newDialog):
		self._dialog_pos = newDialog


	# sets noun phrases
	def SetNounPhrases(self, phrases):
		self._nounPhrases = phrases


	# sets synonyms provider for this report
	def SetSynonymsProvider(self, provider):
		self._synonymsProvider = provider


	def SetSynonymSimilarity(self, similarity):
		self._synonymSimilarity = similarity


	# loads noun phrases and caches them in array
	def LoadNounPhrases(self):
		report = nounPhrasePartsReport.NounPhraseParts(self._outputDir)
		report.SetDialog(self._dialog_pos)
		self._nounPhrases = report.ExtractNounPhrases()


	# returns list with used nouns per person (raw version not using WordNet)
	def FindUsedNounsRaw(self):
		people = personDialog.Person()
		# dont do anything unless everything is properly set up
		# check, if noun phrases were loaded
		if self._nounPhrases is None:
			self.LoadNounPhrases()

		# check the noun phrases one more time - if they arent loaded up, then there arent any
		if self._nounPhrases is None:
			return None

		# prepare data structure
		helper = helperDialog.Helper()
		listPeople = helper.GetListPeople(self._dialog.GetDialog())
		result = {}
		for person in listPeople:
			result['{}-{}'.format(person[1], person[0])] = people.GetEmptyNounsPerson(person[1], person[0], {})

		for phrase in self._nounPhrases:
			for word in phrase['nouns']:
				if word in self._stopwords: # skip stopwords
					continue

				key = '{}-{}'.format(phrase['name'], phrase['role'])
				if word in result[key]['nouns'].keys():
					result[key]['nouns'][word] += 1
				else:
					result[key]['nouns'][word] = 1

		# sort results for each person
		for key in result.keys():
			if len(result[key]['nouns'].keys()):
				# first, conert it to list of tuples
				result[key]['nouns'] = [(noun, result[key]['nouns'][noun]) for noun in result[key]['nouns'].keys()]
				result[key]['nouns'].sort(key = lambda x: x[1], reverse = True)
			else:
				result[key]['nouns'] = []

		return result

	# cluster results of this report using synonyms provider
	def clusterResultsByPerson(self, original_data):
		results = {}
		for person in original_data:
			results[person] = {}
			words = original_data[person]['nouns']
			for w in words:
				if w[0] in results[person]:
					results[person][w[0]]['count'] += 1
				else:
					found = False
					synonyms = self._synonymsProvider.GetSynonyms(w[0])
					for w_s in synonyms:
						if w_s in results[person]:
							results[person][w_s]['count'] += 1
							found = True
						else:
							for record in results[person]:
								if w_s in results[person][record]['synonyms']:
									results[person][record]['count'] += 1
									found = True
									break
						if found:
							break

					if not found:
						results[person][w[0]] = {
										'count' : 1,
										'synonyms' : synonyms
											}
		return results

	# cluster results of this report using synonyms provider
	def clusterResultsByWord(self, original_data):
		results = {}
		for person in original_data:
			words = original_data[person]['nouns']
			for w in words:
				if w[0] in results:
					results[w[0]]['count'] += 1
				else:
					found = False
					synonyms = self._synonymsProvider.GetSynonyms(w[0])
					for w_s in synonyms:
						if w_s in results:
							results[w_s]['count'] += 1
							found = True
						else:
							for record in results:
								if w_s in results[record]['synonyms']:
									results[record]['count'] += 1
									found = True
									break
						if found:
							break

					if not found:
						results[w[0]] = {
									'count' : 1,
									'synonyms' : synonyms
										}
		return sorted([(w, results[w]['count']) for w in results.keys()], key=lambda x:x[1], reverse=True)


	# this method saveds data produced by this report to a CSV file
	def SaveToFile(self, data, name = None):
		fileName = 'usednouns.csv'
		if name != None:
			fileName = name + ".csv"

		with open(self._outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(['Role', 'Name', 'Noun', 'Count'])
			for idx in data.keys():
				row = data[idx]
				if len(row['nouns']):
					for nounTuple in row['nouns']:
						writer.writerow([row['role'], row['name'], nounTuple[0], nounTuple[1]])


	def SaveToFileClusteredByPerson(self, data, name=None):
		fileName = 'usednouns_by_person.csv'
		if name != None:
			fileName = name + ".csv"

		with open(self._outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			writer.writerow(['Role', 'Name', 'Noun', 'Count'])
			for idx in data.keys():
				data_person = idx.split('-')
				person = data[idx]
				for w in person:
					writer.writerow([data_person[1], data_person[0], w, person[w]['count']])


	def SaveToFileClusteredByWord(self, data, name=None):
		fileName = 'usednouns_by_word.csv'
		if name != None:
			fileName = name + ".csv"

		with open(self._outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			writer.writerow(['Noun', 'Count'])
			for w in data:
				writer.writerow([w[0], w[1]])
