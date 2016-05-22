import pandas as pd
import numpy as np
import math

# my tools
from tools.parsers import mpqa as mpqaParser


# class that prepares data for training and testing phase
class Preparation(object):

    # constructor
    def __init__(self):
        self.cutoffNeutralSentiment = 0.005
        # constants for calculation of sentiment based on provided annotations
        self.sentimentConstants = {
            'intensity' : {
                            'low' : 0.2,
                            'medium' : 0.5,
                            'high' : 1,
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
                            'other-attitude' : 0.00001,
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
        annotations = self.CorrectAnnotationsDataFrame(annotations)

        counter = 0
        sentColumns = ['sentiment-measured', 'sentiment-type', 'sentiment-intensity']
        sentimentResults = pd.DataFrame(np.zeros((sentences.shape[0], 3)), columns = sentColumns)
        self.counter = 0
        self.counter2 = 0
        self.counter3 = 0
        for index, sentence in sentences.iterrows():
            sentimentResults['sentiment-measured'][index] = 0 # by default, we assume that the sentence has no sentiment
            currentAnnots = annotations[(annotations['docName'] == sentence['docName']) & (annotations['dirName'] == sentence['dirName']) & (annotations['startByte'] >= sentence['startByte'] ) & (annotations['endByte'] <= sentence['endByte']) ]
            if len(currentAnnots.index) > 0:
                measured, sentimentType, intensity = self._calculateSentimentSentenceAnnotations(sentence, currentAnnots)
                sentimentResults['sentiment-measured'][index] = measured
                sentimentResults['sentiment-type'][index] = sentimentType
                sentimentResults['sentiment-intensity'][index] = intensity
#                print(measured)
#                print(sentimentType)
#                print(intensity)
            else:
                continue
#            print("############################")
#            if counter > 0:
#                return
#            else:
#                counter += 1
        print('Counter = {}'.format(self.counter))
        print('Counter2 = {}'.format(self.counter2))
        print('Counter3 = {}'.format(self.counter3))
        return pd.concat([sentences, sentimentResults], axis = 1)


    # takes sentences and replaces word constants in columnts with numbers (plus, replaces NAs with 'unknown' constants)
    def CorrectAnnotationsDataFrame(self, annotations):
        annotations.fillna(value = "unknown", inplace = True)
        for column in annotations.columns: # go through all columns and replace values with proper constants
            if column in self.sentimentConstants.keys():
                annotations[column] = annotations[column].map(lambda cell: self.sentimentConstants[column].get(cell))

        return annotations

    # calculates sentiment from provided annotations
    # returns 3 values
    # --- whether the sentiment is measurable
    # --- what kind of sentiment is it (mixes positive and negative, or one of those)
    # --- range of the sentiment
    def _calculateSentimentSentenceAnnotations(self, sentence, annotations):
        measured = 0
        sentimentType = 0
        sentimentIntensity = 0
        # calculate frequencies of values by columns (which are used)
        attitudeType = annotations['attitude-type'].value_counts()
        attitudeUncertain = annotations['attitude-uncertain'].value_counts()
        polarity = annotations['polarity'].value_counts()

        # check, if the sentiment is measurable
        otherAttitude = attitudeType.get(self.sentimentConstants['attitude-type']['other-attitude'], 0) > 0
        other = attitudeType.get(self.sentimentConstants['attitude-type']['other'],0) > 0
        if other or otherAttitude:
            somewhatUncertain = attitudeUncertain.get(self.sentimentConstants['attitude-uncertain']['somewhat-uncertain'], 0)
            veryUncertain = attitudeUncertain.get(self.sentimentConstants['attitude-uncertain']['very-uncertain'], 0)
            if ((somewhatUncertain + veryUncertain) * 5.0) / 8.0: # not certain about the sentiment, so it is not measurable
                return (measured, sentimentType, sentimentIntensity)
        # there is still chance to measure sentiment
        measured = 1

        # check, what type of sentiment is used in the sentence
        polarityBoth = polarity.get(self.sentimentConstants['polarity']['both'], 0)
        polarityShape = annotations.shape[0] - polarity.get(self.sentimentConstants['polarity']['unknown'], 0)
        if (polarityBoth * 1.4) < annotations.shape[0]: # so the annotations suggest that the sentence has mixed sentiment
            sentimentType = 1

        # last, but not least, calculate the intensity of sentiment
        if sentimentType == 1:
            annotsFiltered = annotations[(annotations['polarity'] != self.sentimentConstants['polarity']['both']) & (annotations['polarity'] != self.sentimentConstants['polarity']['uncertain-both'])]
            annotsNeutral = annotsFiltered[annotsFiltered['polarity'] == self.sentimentConstants['polarity']['neutral']]
            annotsNeutralUncertain = annotsFiltered[annotsFiltered['polarity'] == self.sentimentConstants['polarity']['uncertain-neutral']]
            if (annotsNeutral.shape[0] + annotsNeutralUncertain.shape[0]) >= ((annotsFiltered.shape[0] * 3.0) / 4): # the sentiment is rather neutral
                return (measured, sentimentType, sentimentIntensity)

            # the sentiment is either positive, or negative
            positive = np.array([])
            negative = np.array([])
            for idx, row in annotsFiltered.iterrows():
                calculated = self._calculateIntensityAnnotation(row)
                if calculated < 0:
                    negative = np.append(negative, [-calculated])
                else:
                    positive = np.append(positive, [calculated])

            # calculate mean of each values and pick the strongest one
            meanNegative = 0
            meanPositive = 0
            if negative.size > 0:
                meanNegative = np.mean(negative)
            if positive.size > 0:
                meanPositive = np.mean(positive)
#            # check this sentence, if it has negative sentiment
            if abs(meanPositive - meanNegative) > self.cutoffNeutralSentiment:
                if meanNegative > meanPositive:
                    sentimentIntensity = -meanNegative
                else:
                    sentimentIntensity = meanPositive
            else:
                self.counter += 1
        else: # mixes sentiment
#            annotsFiltered = annotations[annotations['polarity'] == self.sentimentConstants['polarity']['both']]
            vals = np.array([])
            for idx, row in annotations.iterrows():
                if row['polarity'] == self.sentimentConstants['polarity']['both'] or row['polarity'] == self.sentimentConstants['polarity']['uncertain-both']:
                    vals = np.append(vals, [self._calculateIntensityAnnotation(row)])
            if vals.shape[0] > 0:
                self.counter2 += 1
#                print("Vals {}".format(np.mean(vals)))
                sentimentIntensity = np.mean(vals)
            else:
                self.counter3 += 1

        return (measured, sentimentType, sentimentIntensity)


    # calculates intensity of one annotation
    def _calculateIntensityAnnotation(self, annot):
        intensity = annot['polarity']
        if intensity == None:
            intensity = 0.01
        if annot['attitude-type'] != self.sentimentConstants['attitude-type']['unknown']:
            intensity += annot['attitude-type']
            if annot['attitude-uncertain'] != self.sentimentConstants['attitude-uncertain']['unknown']:
                intensity *= annot['attitude-uncertain']

        if annot['intensity'] != self.sentimentConstants['intensity']['unknown']:
            intensity *= annot['intensity']
        if annot['expression-intensity'] != self.sentimentConstants['expression-intensity']['unknown']:
            intensity *= annot['expression-intensity']
        return intensity
