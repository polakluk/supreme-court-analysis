from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

# This class is a wrapper for WordNet Synonyms library
class Wordnet(object):

	# constructor
	def __init__(self):
		self.__similarity = 0.4
		self.__lemmatizer = WordNetLemmatizer()


    # sets value for similarity index
	def SetSimilarity(self, similarity):
		self.__similarity = similarity


    # gets list of synonyms with their respective similarity index as a sorted list of
	def GetSynonyms(self, word):
		synonyms = []

		try:
			wordLemma = self.__lemmatizer.lemmatize(word)
			results = wordnet.synsets(wordLemma, pos='n')

			# get only words
			for record in results:
				for lemma in record.lemmas():
					synonyms.append(str(lemma.name()).lower())

		except WordNetError: # check, if any synonym has been found (if not, return only this word)
			return [word]

		return list(set(synonyms))
