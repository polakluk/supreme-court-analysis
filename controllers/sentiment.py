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
                                'extract-features' : self._extractFeatures
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


    # calculates features from data prepared by method _prepareTrainingData
    # it uses sentences and combined dictionary (General Inquiry + MPQA processed)
    # result of this operation is saved as a CSV file for later use
    def _extractFeatures(self):
        prepData = preparation.Preparation()
        featureVectors = prepData.ExtractFeatures()
        instanceVectors = prepData.AddOutputDataInstancec(featureVectors)

        args = vars(self.argParser.parse_args())
        fileName = args['outputFile']
        if fileName == None:
            fileName = prepData.defaultFileNameSentimentSentences
        prepData.SaveFileCsv(instanceVectors, fileName)
