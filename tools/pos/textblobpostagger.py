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

    def _clean_up_sentence(self, sent):
        if sent[0] in '"()':
            return sent[1:].strip()
        elif sent[:3] == ') (':
            return sent[3:].strip()
        else:
            return sent

    # this method should separate text into sentences
    def SeparateSentenctes(self, text):
        if len(text) == 0:
            return []
        return self._process_sentences(self.__sentence_slicer.sentences_from_text(text, realign_boundaries=False))

    def _process_sentences(self, sentences):
        for idx in range(len(sentences)):
            if sentences[idx][0] == '"':
                newSentences = []
                if idx > 1:
                    newSentences = sentences[:idx - 1]

                separatedSentences = sentences[idx - 1].split(', "')
                if len(separatedSentences) == 1:
                    newSentences += separatedSentences
                    return newSentences

                separatedSentences[0] = separatedSentences[0] + '.'
                newSentences += separatedSentences

                cleanSentence = self._clean_up_sentence(sentences[idx])
                if len(cleanSentence):
                    newSentences += [cleanSentence]

                if len(sentences) > idx:
                    newSentences += sentences[idx + 1:]
                return self._process_sentences(newSentences)

            if sentences[idx][0] == ')':

                newSentences = []
                if idx > 1:
                    newSentences = sentences[:idx - 1]

                if sentences[idx-1].find('(') != -1:
                    pos = len(sentences[idx-1]) - sentences[idx-1][::-1].index('(') - 1
                    parts = [sentences[idx-1][:pos], sentences[idx-1][pos+1:]]

                    for part in parts:
                        if len(part):
                            newSentences += [part]
                else:
                    newSentences += [sentences[idx-1]]
                cleanSentence = self._clean_up_sentence(sentences[idx])
                if len(cleanSentence):
                    newSentences += [cleanSentence]

                if len(sentences) > idx:
                    newSentences += sentences[idx + 1:]
                return self._process_sentences(newSentences)
        return sentences

    # tag each word in provided sentencted
    def Tag(self, sentence, isDebug = False):
        res = []
        tagged_words = TextBlob(sentence, pos_tagger = self.__pos_tagger)
        posSentence = tagged_words.tags
        if len(posSentence) > 0:
            res = posSentence
        if isDebug:
            print("End Tagging")

        return res
