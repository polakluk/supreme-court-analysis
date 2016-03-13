from nltk import pos_tag, word_tokenize
from nltk.tokenize import punkt
from nltk.corpus import stopwords
import string

# This class is a wrapper for NLTK POS tagger
class NltkPos:

	# constructor
	def __init__(self):
		self.__filter_words = []

		for c in string.punctuation:
			self.__filter_words.append(c)
		self.__sentence_slicer = punkt.PunktSentenceTokenizer()


	# this method should separate text into sentencec
	def SeparateSentenctes(self, text):
		return self.__sentence_slicer.sentences_from_text(text, realign_boundaries = False )


	# tag each word in provided sentencted
	def Tag(self, sentences):
		res = []

		for sentence in sentences:
			words = self.__preprocess(word_tokenize(sentence))
			res.append(pos_tag(words))

		return res

	# this method will remove punctuation from array of words
	def __preprocess(self, words):
		filtered_words = [w for w in words if not w in self.__filter_words ]
		return filtered_words
