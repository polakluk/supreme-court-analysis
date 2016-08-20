import controllers.base

# my tools
from tools.filehelper import FileHelper
from tools.dialogs import posdialog as dialogPosDialog
from tools.sentimentanalysis import preparation, featureextract, predict

# Controller for handling sentimen analysis experiments
# Description: Measure, whether the sentiment is negative, positive or neutral
# Result: Real number in range <-1,1> measuring polarity
#           (-1 = utterly negative, 0 = neutral, 1 = utterly positive)
class Sentiment(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                    'prepare-training-data': self._prepareTrainingData,
                    'normalize-values' : self._normalizeValues,
                    'extract-features' : self._featureExtract,
                    'calculate-sentiment' : self._calculateSentiment
        }


    # initializes its own parser
    def initializeArgumentParser(self):
        self.argParser.add_argument('-fout', help="Optional output filename for Feature files", dest="outputFile", required = False)
        self.argParser.add_argument('-fin', help="Optional input filename for sentiment prediction", dest="inpFile", required = False)
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


    # this task extracts all features from sentences
    def _featureExtract(self):
        args = vars(self.argParser.parse_args())
        helper = FileHelper()
        fNameRaw = helper.GetFileName(args['inpFile'])
        extractor = featureextract.FeatureExtract(self.pprint)
        extractor.Initialize()
        dialog = dialogPosDialog.PosDialog(self.parsedDataDir+fNameRaw + self.pathSeparator)
        dialog.LoadFromFile(args['inpFile'])
        dt = dialog.AsDataFrame()
        dt = dt.apply(lambda row: extractor.ExtractFeaturesSentence(row), axis = 1)

        fOutName = args['outputFile']
        if fOutName is None:
            fOutName = self.parsedDataDir + fNameRaw + self.pathSeparator + fNameRaw + ".features"

        dt.to_csv(fOutName)


    # calculates sentiment per file
    def _calculateSentiment(self):
        model = predic.Predict()
    # first, load dialog with POS tags
