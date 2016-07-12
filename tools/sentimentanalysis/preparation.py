import pandas as pd
import numpy as np
import math
import os

# my tools
from tools.parsers import mpqa as mpqaParser
from tools.parsers import generalinquirer as generalInquirerParser


# class that prepares data for training and testing phase
class Preparation(object):

    # constructor
    def __init__(self):
        self.sepDir = os.path.sep
        self.defaultFileNameSentimentSentences = '.'+self.sepDir+'corpora'+self.sepDir+'processed'+self.sepDir+'sentiment-sentences.csv'
        self.defaultFileNameSentimentSentencesNormalized = '.'+self.sepDir+'corpora'+self.sepDir+'processed'+self.sepDir+'sentiment-sentences-norm.csv'
        self.defaultFileNameSentimentSentencesFeatures = '.'+self.sepDir+'featuresData'+self.sepDir+'sentiment-sentences.csv'

        self.cutoffNeutralSentiment = 0.005
        # constants for calculation of sentiment based on provided annotations
        self.sentimentConstants = {
            'intensity' : {
                            'neutral' : 0.1,
                            'low' : 0.2,
                            'low-medium' : 0.35,
                            'medium' : 0.5,
                            'medium-high' : 0.75,
                            'high' : 1,
                            'high-extreme' : 1.5,
                            'extreme' : 2,
                            'unknown' : 0
                        },
            'expression-intensity' : {
                            'neutral' : 1.01,
                            'low' : 1.25,
                            'medium' : 1.5,
                            'high' : 2,
                            'extreme' : 2.5,
                            'unknown' : 1.0
                        },
            'polarity' : {
                        'positive' : 1,
                        'negative' : -1,
                        'both' : 0.9,
                        'neutral' : 0.01,
                        'uncertain-positive' : 0.8,
                        'uncertain-negative' : -.8,
                        'uncertain-both' : 0.75,
                        'uncertain-neutral' : 0.05,
                        'unknown' : 0
            },
            'attitude-type' : {
                            'other' : 0,
                            'other-attitude' : 0.001,
                            'arguing-neg' : -0.75,
                            'arguing-pos' : 0.75,
                            'sentiment-neg' : -0.5,
                            'sentiment-pos' : 0.5,
                            'agree-neg' : -0.25,
                            'agree-pos' : 0.25,
                            'intention-neg' : -0.6,
                            'intention-pos' : 0.6,
                            'specilation' : 0.01,
                            'speculation' : 0.01,
                            'unknown' : -1
            },
            'attitude-uncertain' : {
                            'somewhat-uncertain' : 0.9,
                            'very-uncertain' : 0.5,
                            'unknown' : 1.0
            }
        }


    # assigns sentiment to each sentence from MPQA corpus based on provided annotations
    # the final sentiment is returned as pandas DataFrame
    def AssignSentimentSentences(self):
        # load up both MQPA corpus and MPQA annotations
        parser = mpqaParser.Mpqa()
        sentences = parser.readFileCsv(parser.defaultFileNameProcessed)
        annotations = parser.readFileCsv(parser.defaultFileNameProcessedAnnots)

        counter = 0
        sentColumns = ['sentiment-measured', 'sentiment-type', 'sentiment-intensity']
        sentimentResults = pd.DataFrame(np.zeros((sentences.shape[0], len(sentColumns))), columns = sentColumns)
        # preprocess annotations
        annotations[annotations['attitude-type'].isin(['other', 'other-attitude', 'speculation', 'specilation'])] = np.nan

        for index, sentence in sentences.iterrows():
            if sentence['annotsCount'] == 0: # no annotations = no sentiment
                continue

            currentAnnots = self._filterAnnotations(annotations[(annotations['sentRow'] == index) ])
            if currentAnnots.shape[0] == 0: # are there any meaningful annotations?
                continue

            currentAnnots = self.CorrectAnnotationsDataFrame(currentAnnots)
            sentimentType, intensity = self._calculateSentimentSentenceAnnotations(sentence, currentAnnots)
            sentimentResults['sentiment-measured'][index] = 1
            sentimentResults['sentiment-type'][index] = sentimentType
            sentimentResults['sentiment-intensity'][index] = intensity

        finalFrame = pd.concat([sentences, sentimentResults], axis = 1)
        return finalFrame[finalFrame['annotsCount'] > 0].reset_index()


    # takes sentences and replaces word constants in columnts with numbers (plus, replaces NAs with 'unknown' constants)
    def CorrectAnnotationsDataFrame(self, annotations):
        annotations.fillna(value = "unknown", inplace = True)
        for column in annotations.columns: # go through all columns and replace values with proper constants
            if column in self.sentimentConstants.keys():
                annotations[column] = annotations[column].map(lambda cell: self.sentimentConstants[column].get(cell))

        return annotations


    # normalizes values of detected sentiment
    def NormalizeValues(self):
        parser = mpqaParser.Mpqa()
        sentences = parser.readFileCsv(self.defaultFileNameSentimentSentences)

        # normalize values
        knownSentiment = sentences[sentences['sentiment-measured'] == 1]
        # normalize mixed sentiment
        sentimentMixed = knownSentiment['sentiment-type'] == 1
        minVal = knownSentiment.loc[sentimentMixed, 'sentiment-intensity'].min()
        maxVal = knownSentiment.loc[sentimentMixed, 'sentiment-intensity'].max()
        knownSentiment.loc[sentimentMixed, 'sentiment-intensity'] = knownSentiment.loc[sentimentMixed, 'sentiment-intensity'] - minVal
        rangeValues = float(maxVal - minVal)
        knownSentiment.loc[sentimentMixed, 'sentiment-intensity'] = (rangeValues - knownSentiment.loc[sentimentMixed, 'sentiment-intensity']) / rangeValues

        # now, normalize polarized sentiment
        sentimentPolarized = knownSentiment['sentiment-type'] == 0
        sentimentPolarizedNegative = sentimentPolarized & (knownSentiment['sentiment-intensity'] < 0)
        sentimentPolarizedPositive = sentimentPolarized & (knownSentiment['sentiment-intensity'] > 0)
        minVal = knownSentiment.loc[sentimentPolarized, 'sentiment-intensity'].min()
        maxVal = knownSentiment.loc[sentimentPolarized, 'sentiment-intensity'].max()
        rangeValuesNeg = float(minVal)
        rangeValuesPos = float(maxVal)
        knownSentiment.loc[sentimentPolarizedNegative, 'sentiment-intensity'] = ((rangeValuesNeg - knownSentiment.loc[sentimentPolarizedNegative, 'sentiment-intensity']) / -rangeValuesNeg)
        knownSentiment.loc[sentimentPolarizedPositive, 'sentiment-intensity'] = (rangeValuesPos - knownSentiment.loc[sentimentPolarizedPositive, 'sentiment-intensity']) / rangeValuesPos

        return knownSentiment


    # the method takes annotations and filters out meaningless annotations
    # returns filtered annotations
    def _filterAnnotations(self, annotations):
        filterIndex = (np.invert(annotations['polarity'].isnull())) | (np.invert(annotations['attitude-type'].isnull()))
        return annotations[filterIndex]


    # calculates sentiment from provided annotations
    # returns 2 values
    # --- what kind of sentiment is it (mixes positive and negative, or one of those)
    # --- range of the sentiment
    def _calculateSentimentSentenceAnnotations(self, sentence, annotations):
        sentimentType = 0
        sentimentIntensity = 0

        # calculate intensities of annotations
        annotsValues = annotations.apply(lambda row: self._calculateIntensityAnnotation(row), axis = 1)
        negative = annotsValues[annotsValues < 0]
        positive = annotsValues[annotsValues >= 0]
        # if both type of annotations are present, then the sentiment is mixed
        if (negative.shape[0] > 0) & (positive.shape[0] > 0):
            sentimentType = 1

        if sentimentType == 1:
            negSum = negative.sum()
            posSum = positive.sum()
            sentimentIntensity = negSum + posSum
        else:
            # take mean of annotations
            sentimentIntensity = np.mean(annotsValues)
            if abs(sentimentIntensity) < self.cutoffNeutralSentiment:
                sentimentIntensity = 0

        return (sentimentType, sentimentIntensity)


    # calculates intensity of one annotation
    def _calculateIntensityAnnotation(self, annot):
        intensity = 0
        if annot['polarity'] == None: # calculate intensity from attitude
            intensity = annot['attitude-type']
            if annot['attitude-uncertain'] != self.sentimentConstants['attitude-uncertain']['unknown']:
                intensity *= annot['attitude-uncertain']
        else: # primarily focus on calculating intensity from polarity
#            print("********************")
#            print(annot)
            intensity = annot['polarity']
            if annot['intensity'] != self.sentimentConstants['intensity']['unknown']:
                intensity *= annot['intensity']
            if annot['expression-intensity'] != self.sentimentConstants['expression-intensity']['unknown']:
                intensity *= annot['expression-intensity']
        return intensity


    # extracts features from sentences
    def ExtractFeatures(self):
        parserMpqa = mpqaProcessedParser.MpqaProcessed()
        parserInquirer = generalInquirerParser.GeneralInquirer()
        sentences = parserMpqa.readFileCsv(parserMpqa.defaultFileNameProcessed)
        sentimentDictionaries = parserInquirer.readFileCsv(parserInquirer.combinedFileLoc)

        return pd.DataFrame({})


    # adds output vectors to feature vectors
    def AddOutputDataInstancec(self, features):
        parserMpqa = mpqaProcessedParser.MpqaProcessed()
        sentences = parserMpqa.readFileCsv(parserMpqa.defaultFileNameProcessed)
        outputData = sentences[:,('sentiment-measured', 'sentiment-type','sentiment-intensity')]

        return features


    # saves the data with header to a file in CSV format
    def SaveFileCsv(self, data, fileName):
        with open(fileName, 'wb') as csvfile:
            data.to_csv(csvfile, index = False)
