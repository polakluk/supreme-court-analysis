from nltk.corpus import wordnet
from nltk.corpus import lin_thesaurus as thes
from nltk.stem.wordnet import WordNetLemmatizer

# This class is a wrapper for WordNet Dekang Lin
class Lin(object):

	# constructor
	def __init__(self):
		self.__similarity = 0.03
		self.__max_words = 5
		self.__lemmatizer = WordNetLemmatizer()
		self.__fileId = 'simN.lsp'
		self.__use_lemma = True
		self.__found_synonyms = {}

    # sets value for similarity index
	# it shows what is the maximum difference between best match and the "last picked matxh"
	def SetSimilarity(self, similarity):
		self.__similarity = similarity

    # sets value for max number of synonyms
	def SetMaxWords(self, max_words):
		self.__max_words = max_words

	def SetUseLemma(self, lemma):
		self.__use_lemma = lemma

	def _get_configuration_key(self):
		return '{}-{}-{}'.format(self.__similarity, self.__max_words, self.__use_lemma)

    # gets list of synonyms with their respective similarity index as a sorted list of
	def GetSynonyms(self, word):
		try:
			# check, if the result is not cached
			current_key = self._get_configuration_key()
			if current_key not in self.__found_synonyms:
				self.__found_synonyms[current_key] = {}

			if word in self.__found_synonyms[current_key]:
				return self.__found_synonyms[current_key][word]

			# it is not, so find synonyms
			wordLemma = word
			if self.__use_lemma:
				wordLemma = self.__lemmatizer.lemmatize(word)
			results = thes.scored_synonyms(wordLemma, fileid=self.__fileId)
			if len(results) > 0:
				sorted_results = sorted(results, key=lambda cell: cell[1], reverse=True)
				final_results = [w[0].lower() for w in sorted_results if (sorted_results[0][1] - w[1]) <= self.__similarity]
				if self.__max_words > 0 and len(final_results) > self.__max_words:
					final_results = final_results[:self.__max_words]
				if word.lower() not in final_results:
					final_results.append(word)

				self.__found_synonyms[current_key][word] = final_results
				return final_results
			else: # no synonym found
				return [word]

			return filtered_results
		except: # check, if any synonym has been found (if not, return only this word)
			return [word]
