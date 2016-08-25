from tools.dialogs import person as personDialog
from tools.dialogs import helper as helperDialog
from tools.reports.nlp import topicchainindex as topicChainIndexReport
from tools.reports.nlp import usednounsperson as usedNounsPersonReport


# this class prepares reports from loaded dialog
# REPORT Description:
# The report returns list of nouns grouped by synonyms.
# Under the hood, it takes TCI for each person and concats them
class GroupSynonymsTci(object):

	# constructor
	def __init__(self, reportsDir):
		self.__outputDir = reportsDir
		self.__dialog = None
		self.__dialog_pos = None
		self.__simProvider = None


	# sets dialog for this report
	def SetDialog(self, newDialog):
		self.__dialog = newDialog


	# sets POS dialog for this report
	def SetDialogPos(self, newDialog):
		self.__dialog_pos = newDialog


	# sets similarity provider
	def SetSimProvider(self, provider):
		self.__simProvider = provider


	# returns list with noun phrases
	# param chains - list of chains from report TopicChainIndex
	def GroupTci(self, chainsReport):
		people = personDialog.Person()
		# dont do anything unless everything is properly set up
		parts = self.__dialog.GetDialogPos()
		if parts == None:
			return None

		helper = helperDialog.Helper()
		result = []
		# first, extract nouns
		report1 = usedNounsPersonReport.UsedNounsPerson(self.__outputDir)
		report1.SetDialog(self.__dialog)
		nouns = report1.FindUsedNounsRaw()

		# then, create topic chains
		chains = {}
		for record in chainsReport:
			if record != None:
				chains[row['word']] = row['result']

		# now, join topic chains using synonyms
		merged = 0
		for idxChain in chains.keys():
			similar = self.__simnProvider.GetSimilarWords(idxChain)
			print(chain)
			print("************** For Word - " + chain['word'])
			print(similar)
			chainSimilar = [ chain['name'] + "|" + chain['role'] + '|' + sim for sim in similar ]
			# there is a match for this simialar word
			for newChain in chainSimilar:
				# do not check for the current chain
				if newChain == idxChain:
					continue

				for searchIdx in chains.keys():
					if searchIdx == idxChain:
						continue

					# there is a chain with thi synonym
					if searchIdx == newChain:
						if chains[idxChain][0]['result']['startPos'] > chains[searchIdx][0]['result']['startPos']:
							chains[idxChain][0]['result']['startPos'] = chains[searchIdx][0]['result']['startPos']
						if chains[idxChain][0]['result']['lastPos'] < chains[searchIdx][0]['result']['lastPos']:
							chains[idxChain][0]['result']['lastPos'] = chains[searchIdx][0]['result']['lastPos']

						chains[idxChain][0]['result']['count'] += chains[searchIdx][0]['result']['count']
						chains[idxChain][0]['result']['length'] = chains[idxChain][0]['result']['lastPos'] - chains[idxChain][0]['result']['startPos']

						# the last thing you do is to delete the synonym chain
						del chains[searchIdx]
						merged += 1
						continue

		print("Merged TCI: "+str(merged))

		return chains


	# saves the report to file
	def SaveToFile(self, data):
		return None
