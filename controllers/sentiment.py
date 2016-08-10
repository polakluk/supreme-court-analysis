import controllers.base

# my tools
from tools.sentimentanalysis import preparation

# Controller for handling sentimen analysis experiments
# Sentiment analysis steps:
#
# Step 1
#
# Description: Decide, whether the sentiment is (both positive and negative in sentence) or measurable
# Result:  0 -> both positive and negative in sentence (go to Step 2A)
#           1 -> measurable (measure it in Step 2B)
#
# Step 3A
# Description: Measure intensity of mixed sentiment in sentence
# Result: Real number in range (0,1> measuring the intensity
#
# Step 3B
# Description: Measure, whether the sentiment is negative, positive or neutral
# Result: Real number in range <-1,1> measuring polarity
#           (-1 = utterly negative, 0 = neutral, 1 = utterly positive)
class Sentiment(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'prepare-training-data': self._prepareTrainingData,
                                'normalize-values' : self._normalizeValues
        }


    # initializes its own parser
    def initializeArgumentParser(self):
        self.argParser.add_argument('-fout', help="Optional output filename for Feature files", dest="outputFile", required = False)
        self.parserInitialized = True


    # prepare training data (set sentiment for sentences)
    def _prepareTrainingData(self):
        prepData = preparation.Preparation()
        sentiment = prepData.AssignSentimentSentences()
        prepData.SaveFileCsv(sentiment, prepData.defaultFileNameSentimentSentences)


    # normalizes data to range <0,1> (or <-1, 1> for polarized sentiment)
    def _normalizeValues(self):
        prepData = preparation.Preparation()
        data = prepData.NormalizeValues()
        prepData.SaveFileCsv(data, prepData.defaultFileNameSentimentSentencesNormalized)
