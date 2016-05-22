import controllers.base

# my tools
from tools.sentimentanalysis import preparation

# Controller for handling sentimen analysis experiments
# Sentiment analysis steps:
#
# Step 1
#
# Description: Decide, whether the sentiment can be measured
# Result: 0 -> No measured sentiment,
#           1 -> There is some sentiment
#
# Step 2
#
# Description: Decide, whether the sentiment is (both positive and negative in sentence) or measurable
# Result:  0 -> both positive and negative in sentence (go to Step 3B)
#           1 -> measurable (measure it in Step 3B)
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
        }
        self.defaultFileNameSentimentSentences = '.'+self.pathSeparator+'corpora'+self.pathSeparator+'processed'+self.pathSeparator+'sentiment-sentences.csv'


    # initializes its own parser
    def initializeArgumentParser(self):
        # no optional argument added to command-line
        self.parserInitialized = True


    # prepare training data (set sentiment for sentences)
    def _prepareTrainingData(self):
        prepData = preparation.Preparation()
        sentiment = prepData.AssignSentimentSentences()
        with open(self.defaultFileNameSentimentSentences, 'wb') as csvfile:
            sentiment.to_csv(csvfile, index = False)
