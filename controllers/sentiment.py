import pandas as pd
import controllers.base
#other tools
from os import walk
import pandas as pd

# my tools
from tools.filehelper import FileHelper
from tools.filehelper import merger as mergerHelper
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
                    'calculate-sentiment' : self._calculateSentiment,
                    'calculate-per-turn' : self._calculateSentimentPerTurn,
                    'calculate-sentiment-all-files' : self._calculateSentmentAllTurns,
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
        dt.fillna(0, inplace = True)

        fOutName = args['outputFile']
        if fOutName is None:
            fOutName = self.parsedDataDir + fNameRaw + self.pathSeparator + fNameRaw + ".features"

        dt.to_csv(fOutName)


    # calculates sentiment per file
    def _calculateSentiment(self):
        args = vars(self.argParser.parse_args())
        helper = FileHelper()
        fNameRaw = helper.GetFileName(args['inpFile'])
        model = predict.Predict()
        model.LoadModel()

        dt = pd.read_csv(args['inpFile'])
        predicted = model.Predict(dt)
        dt['sentiment'] = predicted
        fOutName = args['outputFile']
        if fOutName is None:
            fOutName = self.parsedDataDir + fNameRaw + self.pathSeparator + fNameRaw + ".sentiment"
        dt.to_csv(fOutName)


    # calculate sentiment per turn based on sentence sentiment
    def _calculateSentimentPerTurn(self):
        args = vars(self.argParser.parse_args())
        helper = FileHelper()
        fNameRaw = helper.GetFileName(args['inpFile'])
        model = predict.Predict()

        fDialogName = self.parsedDataDir + fNameRaw + self.pathSeparator + fNameRaw + ".dialog"
        dt_dialog = pd.read_csv(fDialogName)
        dt_dialog['turn'] = dt_dialog.index
        dt_sentiment = pd.read_csv(args['inpFile'])

        dt_dialog = model.CalculateByTurns(dt_sentiment, dt_dialog)
        dt_dialog.to_csv(fDialogName, index = False)

    # calculate sentiment for all cases
    def _calculateSentmentAllTurns(self):
        merger = mergerHelper.Merger()
        args = vars(self.argParser.parse_args())
        helper = FileHelper()
        model = predict.Predict()
        for (dirpath, dirnames, filenames) in walk(args['inpFile']):
            for dir_name in dirnames:
                self.pprint.pprint('{} - {} ==> {}'.format(dirpath, dir_name, filenames))
                fNameRaw = helper.GetFileName(args['inpFile'])

                fDialogName = dirpath + dir_name + self.pathSeparator + dir_name + ".dialog"
                dt_dialog = pd.read_csv(fDialogName)
                dt_dialog['idx'] = dt_dialog.index
                dt_dialog['docket'] = dir_name
                merger.add_dataframe(dt_dialog)

        merger.export_dataframe(args['outputFile']+'dialog.csv')
