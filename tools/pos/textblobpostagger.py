from nltk.tokenize import punkt
import string

from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

# This class is a wrapper for NLTK POS tagger
class TextBlobPosTagger(object):

    # constructor
    def __init__(self):
        self.__pos_tagger = PerceptronTagger()
        self.__sentence_slicer = punkt.PunktSentenceTokenizer()


    # this method should separate text into sentences
    def SeparateSentenctes(self, text):
        return self.__sentence_slicer.sentences_from_text(text, realign_boundaries = False )


    # tag each word in provided sentencted
    def Tag(self, sentences, isDebug = False):
        res = []

        for sentence in sentences:
            tagged_words = TextBlob(sentence, pos_tagger = self.__pos_tagger)
            posSentence = tagged_words.tags
            if len(posSentence) > 0:
                res.append(posSentence)
            if isDebug:
                print("End Tagging")

        return res
