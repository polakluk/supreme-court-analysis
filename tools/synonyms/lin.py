from nltk.corpus import wordnet
from nltk.corpus import lin_thesaurus as thes
from nltk.stem.wordnet import WordNetLemmatizer

# This class is a wrapper for WordNet Dekang Lin
class Lin(object):

	# constructor
	def __init__(self):
		self.__similarity = 0.4
		self.__lemmatizer = WordNetLemmatizer()
		self.__fileId = 'simN.lsp'


    # sets value for similarity index
	def SetSimilarity(self, similarity):
		self.__similarity = similarity


    # gets list of synonyms with their respective similarity index as a sorted list of
	def GetSynonyms(self, word):
		try:
			wordLemma = self.__lemmatizer.lemmatize(word)
			results = thes.scored_synonyms(wordLemma, fileid=self.__fileId)
			filtered_results = [(rec[0], rec[1]) for rec in results if rec[1] >= self.__similarity]
			if len(filtered_results) > 0:
				return [word for word in sorted(filtered_results, key = lambda x: x[1], reverse = True)]
			else: # no synonym found
				return [word]

			return filtered_results


		except WordNetError: # check, if any synonym has been found (if not, return only this word)
			return [word]
