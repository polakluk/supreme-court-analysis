import pandas as pd
import numpy as np
import string

# my tools
from tools.parsers import mpqa as mpqaParser
from tools.parsers import generalinquirer as generalInquirerParser
from tools.parsers import negation as negationParser
from tools.sentimentanalysis import preparation

# NLTK tools
from nltk import word_tokenize
from nltk.util import ngrams
from nltk.stem.snowball import SnowballStemmer

# class that extracts featuers from a sentence
class FeatureExtract(object):

    # constructor
    def __init__(self, pprinter):
        # constants
        self.__colTextArr = 'textArr'
        self.__colTextArrStemmed = 'textArrStemmed'
        self.__colTokens = 'textArrStemmed'
        self.__colText = 'text'
        self.__colTextPos = 'textPos'
        self.__colTextStemmed = 'textStemmed'

        self.__stemmer = SnowballStemmer("english")
        self.__prepData = preparation.Preparation()
        self.__parserInquirer = generalInquirerParser.GeneralInquirer()
        self.__parserNegation = negationParser.Negation()

        self.__cached_directories = {}


    # initialize extractor (all dictionaries)
    def Initialize(self):
        self.__sentimentDictionary  = self.__parserInquirer.readFileCsv(parserInquirerself.__.combinerowileLoc)
        self.__negations = self.__parserNegation.readFileCsv(self.__parserNegation.defaultFileNameProcessed)

        self.__sentimentDictionary['entryRaw'] = self.__sentimentDictionary['entry']
        self.__sentimentDictionary['entry'] = self.__sentimentDictionary['entry'].map(lambda cell: self.__stemmer.stem(cell))
        self.__sentimentDictionary = self._duplicate_attributes_directory(self.__sentimentDictionary)
        self.__sentimentDictionary.drop_duplicates(subset = 'entry', inplace = True)


    # extracts features from a sentence
    def ExtractFeaturesSentence(self, row):
        # determine punctuation
        row = self._get_punctuation(row)

        # now, preprocess the sentence
        row = self._process_words(row)
        # and remove articles
        row = self._remove_articles(row)

        # count negations
        row = self.__count_negations(row)
        # then, calculate occurances of words from different subsets of dictionary
        row = self._calculate_required_sentence_column_counts(row)
        # moving on to calculate words around negations
        row = self._calculate_required_sentence_words_around_negations(row)
        # and dominant groups of words
        row = self._calculate_required_more_than_other(row)

        # N-grams
        # first, create n-grams
        row = self._generate_n_grams_sentence(row)
        # then, calculate statistics
        row = self._calculate_required_before_after_ngrams_sentence(row)
        # now, generate POS N-grams
        row = self._create_required_n_grams_pos(row)
        # and calculate statistics for them too
        row = self._generate_required_pos_stats(row)

        return row


    # this method implements binary search to look for a value in Series
    def _bin_search__value(self, row, val, start, end, isDebug = False):
        while start <= end:
            if isDebug:
                print("Start: {};    End: {}".format(start, end))
            middle = (start + end) / 2
            if isDebug:
                print("middle: {}".format(row[middle]))
            if row[middle] == val:
                return True
            else:
                if row[middle] > val:
                    end = middle - 1
                else:
                    start = middle + 1
        return False


    # this method actually counts number of selected words (in dictionary) in sentence
    def _count_occurence_in_sentence(self, row, lookFor, lookForLen, columnName):
        words = row[self.__colTextArr]
        res = [word for word in words if self._bin_search_value(lookFor, word, 0, lookForLen)]
        row[columnName] = len(res)
        return row


    # this method prepares counting words from dictionary in a sentnce
    def _calculate_sentence_counts(self, column, row, val = None, typeWord = None):
        compareVal = column
        if column is None:
            columnName = "All"+typeWord
        else:
            if val is not None:
                compareVal = val
            columnName = column+'Count'
            if val is not None:
                columnName = columnName + val
            if typeWord !is not None:
                columnName = columnName + typeWord

        # cache the results for later use
        if columnName not in self.__cached_directories.keys():
            if typeWord is None:
                self.__cached_directories[columnName] = self.__sentimentDictionary[self.__sentimentDictionary[column] == compareVal]
            else:
                if column is None:
                    self.__cached_directories[columnName] = self.__sentimentDictionary[(self.__sentimentDictionary['type'] == typeWord)]
                else:
                    self.__cached_directories[columnName] = self.__sentimentDictionary[(self.__sentimentDictionary[column] == compareVal) & (self.__sentimentDictionary['type'] == typeWord)]

        lookFor = self.__cached_directories[columnName]

        lookForVals = lookFor['entry'].values
        lookForLen = len(lookForVals) - 1
        row = self._count_occurence_in_sentence(row, lookForVals, lookForLen, columnName), axis = 1)

        return row


    # count all requested frequencies of words from dictionary in sentence
    # NOTE: I decided to leave calculating of all features in place. In case there is a change in model,
    # there will not be a need to change this method unless some new features are added
    def _calculate_required_sentence_column_counts(self, row):
        row = self._calculate_sentence_counts('priorpolarity', row, 'negative')
        row = self._calculate_sentence_counts( 'priorpolarity', row, 'both')
        row = self._calculate_sentence_counts( 'priorpolarity', row, 'neutral')
        row = self._calculate_sentence_counts( 'priorpolarity', row, 'positive')
        row = self._calculate_sentence_counts( 'priorpolarity', row, 'negative', 'strongsubj')
        row = self._calculate_sentence_counts( 'priorpolarity', row, 'positive', 'strongsubj')
        row = self._calculate_sentence_counts( 'priorpolarity', row, 'neutral', 'strongsubj')
        row = self._calculate_sentence_counts( 'priorpolarity', row, 'both', 'strongsubj')
        row = self._calculate_sentence_counts( 'priorpolarity', row, 'negative', 'weaksubj')
        row = self._calculate_sentence_counts( 'priorpolarity', row, 'positive', 'weaksubj')
        row = self._calculate_sentence_counts( 'priorpolarity', row, 'both', 'weaksubj')
        row = self._calculate_sentence_counts( 'priorpolarity', row, 'neutral', 'weaksubj')
        row = self._calculate_sentence_counts( None, row, None, 'weaksubj')
        row = self._calculate_sentence_counts( None, row, None, 'strongsubj')
        row = self._calculate_sentence_counts( 'hostile', row, None, 'weaksubj')
        row = self._calculate_sentence_counts( 'strong', row, None, 'weaksubj')
        row = self._calculate_sentence_counts( 'hostile', row, None, 'strongsubj')
        row = self._calculate_sentence_counts( 'strong', row, None, 'strongsubj')
        row = self._calculate_sentence_counts( 'hostile', row)
        row = self._calculate_sentence_counts( 'strong', row)
        row = self._calculate_sentence_counts( 'active', row, None, 'weaksubj')
        row = self._calculate_sentence_counts( 'passive', row, None, 'weaksubj')
        row = self._calculate_sentence_counts( 'active', row, None, 'strongsubj')
        row = self._calculate_sentence_counts( 'passive', row, None, 'strongsubj')
        row = self._calculate_sentence_counts( 'active', row)
        row = self._calculate_sentence_counts( 'passive', row)
        row = self._calculate_sentence_counts( 'positiv', row, None, 'weaksubj')
        row = self._calculate_sentence_counts( 'negativ', row, None, 'weaksubj')
        row = self._calculate_sentence_counts( 'positiv', row, None, 'strongsubj')
        row = self._calculate_sentence_counts( 'negativ', row, None, 'strongsubj')
        row = self._calculate_sentence_counts( 'positiv', row)
        row = self._calculate_sentence_counts( 'negativ', row)
        row = self._calculate_sentence_counts( 'yes', row)
        row = self._calculate_sentence_counts( 'no', row)

        return row


    # counts negations in the sentence
    def _count_negations(self, row):
        words = row[self.__colTextArrStemmed]
        self.__negations['found'] = self.__negations.apply(lambda rowNeg: 1 if rowNeg['phraseStemmed'] in words else 0, axis = 1)
        row['negations'] = negations['found'].sum()
        return row


    # this method duplicates attributes in sentiment word directory before duplicate entries are removed
    def _duplicate_attributes_directory(self, directory):
        checkCategories = ['positiv', 'negativ', 'active', 'passive', 'affil', 'hostile', 'strong',
                           'power', 'weak', 'submit', 'yes', 'no',
                           'negate', 'intrj', 'pleasur', 'pain', 'feel', 'need', 'persist']
        # copy categories among duplicate words in dictionary
        idx = 0
        while idx < directory.shape[0] - 1:
            found = {}
            for key in checkCategories:
                found[key] = directory[key][idx] == key

            idx2 = idx + 1
            while idx2 < directory.shape[0]:
                if directory['entry'][idx] == directory['entry'][idx2]:
                    for key in checkCategories:
                        if directory[key][idx2] == key:
                            found[key] = True
                    idx2 += 1
                else:
                    idx2 -= 1
                    break

            if idx2 == idx:
                idx += 1
            else:
                idx2 += 1
                for key in checkCategories:
                    if found[key] != False:
                        directory[key][idx:idx2] = key

                idx = idx2 + 1
        return directory


    # this method removes articles from sentence
    def _remove_articles(self, row):
        tokens = row[self.__colTextArrStemmed]
        articles = ['a', 'an', 'the']
        tokens = [w for w in tokens if w not in articles]
        row[self.__colTokens] = tokens
        return row


    # cleans up a word from any punctuation
    def _clean_up_word(self, w):
        return w.translate(None, string.punctuation).strip()


    # determines punctuation of a sentence
    def _get_punctuation(row):
        last_character = row[self.__colText][-1:]
        if last_character in '?!.':
            row['punctuation'] = ord(last_character)
        else:
            if last_character in '"\'':
                penultimate_character = row['text'][-2:-1]
                if penultimate_character in '?!.':
                    row['punctuation'] = ord(penultimate_character)
                else:
                    row['punctuation'] = None
            else:
                row['punctuation'] = ord('x')

        return row


    # preprocess words in a sentence
    def _process_words(row):
        words = [ word for word in [self._clean_up_word(w) for w in word_tokenize(row[self.__colText])] if len(word) > 0]
        row[self.__colText] = '|' + '|'.join(words) + '|'
        row[self.__colTextArr] = words

        wordsStemmed = [self.__stemmer.stem(unicode(w, errors='ignore')) for w in words]
        row[self.__colTextStemmed] = '|'.join(wordsStemmed)
        row[self.__colTextStemmed] = '|' + row[self.__colTextStemmed] + '|'
        row[self.__colTextArrStemmed] = wordsStemmed
        return row


    # checkOccurenceColumn
    # this method checks number of occurances of a word from dictionary subset occurs in a sentence before and after any negation
    def _count_occurence_column_in_sentence_before_after(self, row, lookFor, columnName):
        for _, neg_row in self.__negations.iterrows():
            neg = '|'+neg_row['phrase']+'|'
            neg_stemmed = '|' + neg_row['phraseStemmed'] + '|'
            posNeg = row['text'].find(neg)
            if posNeg == -1 :
                return row
            posNeg = row['textStemmed'].find(neg_stemmed)

            afterPos = posNeg + len(neg_stemmed)
            for _, rowLook in lookFor.iterrows():
                posBefore = row['textStemmed'].find(rowLook['entry'], 0, posNeg)
                posAfter = row['textStemmed'].find(rowLook['entry'], afterPos)

                if posBefore != -1:
                    row[columnName+'Before'] = row[columnName+'Before'] + 1
                if posAfter != -1:
                    row[columnName+'After'] = row[columnName+'After'] + 1

        return row

    #WordsAroundNegations
    # this method initialize counting or checking occurances of words from dictionary around negations
    def _words_around_negations_sentence(self, column, row, val = None, count = False):
        columnName = column
        compareVal = val
        if val is None:
            compareVal = column
        else:
            columnName = column + val

        if count:
            columnName = columnName + "Count"

        if columnName not in self.__cached_directories.keys():
            self.__cached_directories[columnName] = self.__sentimentDictionary[self.__sentimentDictionary[column] == compareVal]

        lookFor = self.__cached_directories[columnName]
        if count:
            row[columnName+"Before"]  = 0
            row[columnName+"After"]  = 0

        if count:
            row = self._count_occurence_column_in_sentence_before_after(row, lookFor, columnName)
        else:
            row[columnName+'Before'] = row[columnName + "CountBefore"] > 0
            row[columnName+'After'] = row[columnName + "CountAfter"] > 0

        return row


    # calculates all requested features concerning words from subset of dictionary around negations
    # NOTE: I decided to leave calculating of all features in place. In case there is a change in model,
    # there will not be a need to change this method unless some new features are added
    def _calculate_required_sentence_words_around_negations(self, row):
        row = self._words_around_negations_sentence('active', row, None, True)
        row = self._words_around_negations_sentence('passive', row, None, True)
        row = self._words_around_negations_sentence('hostile', row, None, True)
        row = self._words_around_negations_sentence('yes', row, None, True)
        row = self._words_around_negations_sentence('no', row, None, True)
        row = self._words_around_negations_sentence('negate', row, None, True)
        row = self._words_around_negations_sentence('priorpolarity', row, 'negative', True)
        row = self._words_around_negations_sentence('priorpolarity', row, 'positive', True)
        row = self._words_around_negations_sentence('priorpolarity', row, 'both', True)
        row = self._words_around_negations_sentence('priorpolarity', row, 'neutral', True)

        row = self._words_around_negations_sentence('priorpolarity', row, 'negative')
        row = self._words_around_negations_sentence('priorpolarity', row, 'positive')
        row = self._words_around_negations_sentence('priorpolarity', row, 'neutral')
        row = self._words_around_negations_sentence('priorpolarity', row, 'both')
        row = self._words_around_negations_sentence('active', row)
        row = self._words_around_negations_sentence('passive', row)
        row = self._words_around_negations_sentence('hostile', row)
        row = self._words_around_negations_sentence('yes', row)
        row = self._words_around_negations_sentence('no', row)
        row = self._words_around_negations_sentence('negate', row)
        return row


    # this method generates n-grams
    def _create_n_grams(self, row, size_ngram, prefix = '', field = 'tokens'):
        row[prefix + str(size_ngram)+"_gram"] = list(ngrams(row[field], size_ngram))
        return row


    # generates ordinary n-grams for the sentence
    def _generate_n_grams_sentence(self, row):
        row = self._create_n_grams(row, 2)
        row = self._create_n_grams(row, 3)
        row = self._create_n_grams(row, 4)
        return row


    # countOneBeforeOtherNgranRow
    # counts the number of ngrams in which selected series are one before the other
    def _count_one_before_other_ngran_sentence(self, row, col, size_ngram, beforeSeries, afterSeries):
        # first, try to find a word from "after series"
        n_gram_col = str(size_ngram)+'_gram'
        for n_gram in row[n_gram_col]:
            for idx in range(1, size_ngram):
                w = n_gram[idx]
                found = self._bin_search__value(afterSeries, w, 0, afterSeries.shape[0] - 1)
                if found:
                    for idx_sub in range(0, idx):
                        w2 = n_gram[idx_sub]
                        found_sub = self._bin_search__value(beforeSeries, w2, 0, beforeSeries.shape[0] - 1)
                        if found_sub:
                            row[col] = row[col] + 1
        return row


    # this method initializes counting of ngrams in sentence
    def _count_one_before_other_ngram(self, row, size_ngram, beforeClassCol, afterClassCol, beforeClassVal = None, afterClassVal = None, beforeSerieDefault = None):
        columnName = 'ngram_'+str(size_ngram)+"_"+ beforeClassCol + afterClassCol
        compareValBefore = beforeClassVal
        if beforeClassVal is None:
            compareValBefore = beforeClassCol
        else:
            columnName = columnName + beforeClassVal

        if beforeSerieDefault is None:

            if beforeClassCol+beforeClassVal not in self.__cached_directories.keys():
                self.__cached_directories[beforeClassCol+beforeClassVal] = self.__sentimentDictionary[self.__sentimentDictionary[beforeClassCol] == compareValBefore].reset_index(drop=True)
                self.__cached_directories[beforeClassCol+beforeClassVal] = self.__cached_directories[beforeClassCol+beforeClassVal]['entry']
            lookForBefore = self.__cached_directories[beforeClassCol+beforeClassVal]
        else:
            lookForBefore = beforeSerieDefault

        compareValAfter = afterClassVal
        if afterClassVal is None:
            compareValAfter = afterClassCol
        else:
            columnName = columnName + afterClassVal

        if afterClassCol + afterClassVal not in self.__cached_directories.keys():
            self.__cached_directories[afterClassCol + afterClassVal] = self.__sentimentDictionary[self.__sentimentDictionary[afterClassCol] == compareValAfter].reset_index(drop=True)
            self.__cached_directories[afterClassCol + afterClassVal] = self.__cached_directories[afterClassCol + afterClassVal]['entry']

        lookForAfter = self.__cached_directories[afterClassCol + afterClassVal]

        row[columnName]  = 0
        row = self._count_one_before_other_ngran_sentence(row, columnName, size_ngram, lookForBefore, lookForAfter)
        return row


    # this method calculates all required metrics for ordinary ngrams
    def _calculate_required_before_after_ngrams_sentence(self, row):
        row = self._count_one_before_other_ngram(row, 2, 'negativ', 'priorpolarity', None, 'positive')
        row = self._count_one_before_other_ngram(row, 3, 'negativ', 'priorpolarity', None, 'positive')
        row = self._count_one_before_other_ngram(row, 4, 'negativ', 'priorpolarity', None, 'positive')

        row = self._count_one_before_other_ngram(row, 2, 'negativ', 'priorpolarity', None, 'negative')
        row = self._count_one_before_other_ngram(row, 3, 'negativ', 'priorpolarity', None, 'negative')
        row = self._count_one_before_other_ngram(row, 4, 'negativ', 'priorpolarity', None, 'negative')

        row = self._count_one_before_other_ngram(row, 2, 'negativ', 'priorpolarity', None, 'neutral')
        row = self._count_one_before_other_ngram(row, 3, 'negativ', 'priorpolarity', None, 'neutral')
        row = self._count_one_before_other_ngram(row, 4, 'negativ', 'priorpolarity', None, 'neutral')

        row = self._count_one_before_other_ngram(row, 2, 'negations', 'priorpolarity', None, 'positive', self.__negations['phraseStemmed'])
        row = self._count_one_before_other_ngram(row, 3, 'negations', 'priorpolarity', None, 'positive', self.__negations['phraseStemmed'])
        row = self._count_one_before_other_ngram(row, 4, 'negations', 'priorpolarity', None, 'positive', self.__negations['phraseStemmed'])

        row = self._count_one_before_other_ngram(row, 2, 'negations', 'priorpolarity', None, 'negative', self.__negations['phraseStemmed'])
        row = self._count_one_before_other_ngram(row, 3, 'negations', 'priorpolarity', None, 'negative', self.__negations['phraseStemmed'])
        row = self._count_one_before_other_ngram(row, 4, 'negations', 'priorpolarity', None, 'negative', self.__negations['phraseStemmed'])

        row = self._count_one_before_other_ngram(row, 2, 'negations', 'priorpolarity', None, 'neutral', self.__negations['phraseStemmed'])
        row = self._count_one_before_other_ngram(row, 3, 'negations', 'priorpolarity', None, 'neutral', self.__negations['phraseStemmed'])
        row = self._count_one_before_other_ngram(row, 4, 'negations', 'priorpolarity', None, 'neutral', self.__negations['phraseStemmed'])

        row = self._count_one_before_other_ngram(row, 2, 'hostile', 'priorpolarity', None, 'negative')
        row = self._count_one_before_other_ngram(row, 3, 'hostile', 'priorpolarity', None, 'negative')
        row = self._count_one_before_other_ngram(row, 4, 'hostile', 'priorpolarity', None, 'negative')

        row = self._count_one_before_other_ngram(row, 2, 'persist', 'priorpolarity', None, 'positive')
        row = self._count_one_before_other_ngram(row, 3, 'persist', 'priorpolarity', None, 'positive')

        row = self._count_one_before_other_ngram(row, 2, 'pleasur', 'priorpolarity', None, 'positive')
        row = self._count_one_before_other_ngram(row, 3, 'pleasur', 'priorpolarity', None, 'positive')

        row = self._count_one_before_other_ngram(row, 2, 'weak', 'priorpolarity', None, 'negative')
        row = self._count_one_before_other_ngram(row, 3, 'weak', 'priorpolarity', None, 'negative')

        row = self._count_one_before_other_ngram(row, 2, 'active', 'priorpolarity', None, 'positive')
        row = self._count_one_before_other_ngram(row, 3, 'active', 'priorpolarity', None, 'positive')
        return row


    # this metohd calculates short metrics which checks what group of words is dominant in the sentence
    def _calculate_required_more_than_other(self, row):
        row['morePositiveThanNegativeStrong'] = row['priorpolarityCountpositivestrongsubj'] > row['priorpolarityCountnegativestrongsubj']
        row['morePositiveThanNegativeWeak'] = row['priorpolarityCountpositiveweaksubj'] > row['priorpolarityCountnegativeweaksubj']
        row['morePositiveThanNegative'] = row['priorpolarityCountpositive'] > row['priorpolarityCountnegative']
        row['morePositiveThanNeutral'] = row['priorpolarityCountpositive'] > row['priorpolarityCountneutral']
        row['moreNegativeThanNeutral'] = row['priorpolarityCountnegative'] > row['priorpolarityCountneutral']
        return row


    # create all ngram for POS text
    def _create_required_n_grams_pos(self, row):
        row = self._create_n_grams(row, 4, 'pos_', self.__colTextPos)
        row = self._create_n_grams(row, 5, 'pos_', self.__colTextPos)
        return row


    # counts occurances of one type of POS n-grams before another type of POS n-grams
    def _count_one_before_other_ngran_pos_sentence(self, row, col, size_ngram, beforeSeries, afterSeries, beforeSeriesPos = None, afterSeriesPos = None):
        # first, try to find a word from "after series"
        n_gram_col = 'pos_'+str(size_ngram)+'_gram'
        for n_gram in row[n_gram_col]:
            for idx in range(1, size_ngram):
            w = n_gram[idx]
            if afterSeriesPos is not None and w[1] not in afterSeriesPos:
                continue

            found = self._bin_search__value(afterSeries, w[0], 0, afterSeries.shape[0] - 1)
            if found:
                for idx_sub in range(0, idx):
                w2 = n_gram[idx_sub]
                if beforeSeriesPos is not None and w2[1] not in beforeSeriesPos:
                    continue
                found_sub = self._bin_search__value(beforeSeries, w2[0], 0, beforeSeries.shape[0] - 1)
                if found_sub:
                    row[col] = row[col] + 1
        return row


    #  this method initializes counting POS series one before another
    def _count_one_before_other_ngran_pos(self, row, size_ngram, beforeClassCol, afterClassCol,
                                        beforeClassPos = None, afterClassPos = None,
                                        beforeClassVal = None, afterClassVal = None, beforeSerieDefault = None):
        columnName = 'pos_ngram_'+str(size_ngram)+"_" + '.'.join(beforeClassPos) + '.'.join(afterClassPos)
        if beforeClassCol is not None:
            columnName += beforeClassCol
        if afterClassCol is not None:
            columnName += afterClassCol

        compareValBefore = beforeClassVal
        if beforeClassVal is None:
            compareValBefore = beforeClassCol
        else:
            columnName = columnName + beforeClassVal

        if beforeSerieDefault is None:
            if beforeClassCol is None:
                lookForBefore = sentimentDictionary.reset_index(drop = True)
                lookForBefore = lookForBefore['entryRaw']
            else:
                if beforeClassCol + beforeClassVal not in self.__cached_directories[columnName]:
                    self.__cached_directories[beforeClassCol + beforeClassVal] = self.__sentimentDictionary[self.__sentimentDictionary[beforeClassCol] == compareValBefore].reset_index(drop=True)
                    self.__cached_directories[beforeClassCol + beforeClassVal] = self.__cached_directories[beforeClassCol + beforeClassVal]['entryRaw']
                lookForBefore = self.__cached_directories[beforeClassCol + beforeClassVal]
        else:
            lookForBefore = beforeSerieDefault

        compareValAfter = afterClassVal
        if afterClassVal is None:
            compareValAfter = afterClassCol
        else:
            columnName = columnName + afterClassVal

        if afterClassCol is None:
            lookForAfter = sentimentDictionary.reset_index(drop = True)
            lookForAfter = lookForAfter['entryRaw']
        else:
            if afterClassCol + afterClassVal not in self.__cached_directories[columnName]:
                self.__cached_directories[afterClassCol + afterClassVal] = self.__sentimentDictionary[self.__sentimentDictionary[afterClassCol] == compareValAfter].reset_index(drop=True)
                self.__cached_directories[afterClassCol + afterClassVal] = self.__cached_directories[afterClassCol + afterClassVal]['entryRaw']
            lookForAfter = self.__cached_directories[afterClassCol + afterClassVal]

        row[columnName]  = 0
        row =  self._count_one_before_other_ngran_pos_sentence(row, columnName, size_ngram, lookForBefore, lookForAfter, beforeClassPos, afterClassPos)
        return row


    # generate all statistics about POS ngrams
    def _generate_required_pos_stats(self, row):
        verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        noun_tags = ['NN', 'NNP', 'NNS']
        adjective_tags = ['JJ', 'JJR', 'JJS']
        adjective_adverb_tags = adjective_tags + ['RB', 'RBR', 'RBS']

        row = self._count_one_before_other_ngran_pos(row, 4, None, 'positiv', adjective_tags, noun_tags, None, None)
        row = self._count_one_before_other_ngran_pos(row, 5, None, 'positiv', adjective_tags, noun_tags, None, None)
        row = self._count_one_before_other_ngran_pos(row, 4, None, 'active', adjective_adverb_tags, noun_tags, None, None)
        row = self._count_one_before_other_ngran_pos(row, 5, None, 'active', adjective_adverb_tags, noun_tags, None, None)
        row = self._count_one_before_other_ngran_pos(row, 4, None, 'strong', adjective_tags, noun_tags, None, None)
        row = self._count_one_before_other_ngran_pos(row, 5, None, 'strong', adjective_tags, noun_tags, None, None)
        row = self._count_one_before_other_ngran_pos(row, 5, None, 'negativ', adjective_tags, noun_tags, None, None)
        row = self._count_one_before_other_ngran_pos(row, 4, 'negations', 'priorpolarity', 'ADJ', 'NOUN', None, 'positive', negations['phraseStemmed'])
        row = self._count_one_before_other_ngran_pos(row, 5, 'negations', 'priorpolarity', 'ADJ', 'NOUN', None, 'positive', negations['phraseStemmed'])
        row = self._count_one_before_other_ngran_pos(row, 4, None, 'priorpolarity', adjective_adverb_tags, noun_tags, None, 'positive')
        row = self._count_one_before_other_ngran_pos(row, 5, None, 'priorpolarity', adjective_adverb_tags, noun_tags, None, 'positive')
        row = self._count_one_before_other_ngran_pos(row, 4, None, 'priorpolarity', adjective_adverb_tags, noun_tags, None, 'negative')
        row = self._count_one_before_other_ngran_pos(row, 5, None, 'priorpolarity', adjective_adverb_tags, noun_tags, None, 'negative')
        row = self._count_one_before_other_ngran_pos(row, 4, None, 'priorpolarity', adjective_adverb_tags, noun_tags, None, 'neutral')
        row = self._count_one_before_other_ngran_pos(row, 5, None, 'priorpolarity', adjective_adverb_tags, noun_tags, None, 'neutral')
        row = self._count_one_before_other_ngran_pos(row, 4, None, 'priorpolarity', adjective_tags, noun_tags, None, 'positive')
        row = self._count_one_before_other_ngran_pos(row, 5, None, 'priorpolarity', adjective_tags, noun_tags, None, 'positive')
        row = self._count_one_before_other_ngran_pos(row, 4, None, 'priorpolarity', adjective_tags, noun_tags, None, 'negative')
        row = self._count_one_before_other_ngran_pos(row, 5, None, 'priorpolarity', adjective_tags, noun_tags, None, 'negative')
        row = self._count_one_before_other_ngran_pos(row, 4, None, 'priorpolarity', adjective_tags, noun_tags, None, 'neutral')
        row = self._count_one_before_other_ngran_pos(row, 5, None, 'priorpolarity', adjective_tags, noun_tags, None, 'neutral')
        row = self._count_one_before_other_ngran_pos(row, 4, 'negations', 'priorpolarity', adjective_tags, noun_tags, None, 'positive', negations['phraseStemmed'])
        row = self._count_one_before_other_ngran_pos(row, 5, 'negations', 'priorpolarity', adjective_tags, noun_tags, None, 'positive', negations['phraseStemmed'])
        row = self._count_one_before_other_ngran_pos(row, 4, None, 'hostile', adjective_tags, noun_tags, None, None)
        row = self._count_one_before_other_ngran_pos(row, 5, None, 'hostile', adjective_tags, noun_tags, None, None)
        return row
