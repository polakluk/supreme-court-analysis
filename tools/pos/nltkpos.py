from nltk import pos_tag, word_tokenize
from nltk.tokenize import punkt
from nltk.corpus import stopwords
import string

# This class is a wrapper for NLTK POS tagger
class NltkPos(object):

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
	def Tag(self, sentences, isDebug = False):
		res = []

		for sentence in sentences:
			if isDebug:
				print("Start preprocessing")
			words = self.__preprocess(word_tokenize(sentence))
			if isDebug:
				print("End preprocessing")

			posSentence = [[word[0], word[1]] for word in  pos_tag(words)]
			if len(posSentence) > 0:
				res.append(posSentence)
			if isDebug:
				print("End Tagging")

		return res

	# this method will remove punctuation from array of words
	def __preprocess(self, words):
		filtered_words = [w for w in words if not w in self.__filter_words ]
		return filtered_words
