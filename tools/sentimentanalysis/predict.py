import pandas as pd
import numpy as np
import string
import os

from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
import cPickle as pickle

# class that predicts sentiment based on the model
class Predict(object):

    # constructor
    def __init__(self):
        self.version = '8' # active version of sentiment model
        self.pathSep = os.path.sep
        self._model_path = '.'+self.pathSep + 'models-sentiment' + self.pathSep + 'version_'
        self._model = None
        self._features = []


    # loads current version of model
    def LoadModel(self):
        current_model_path = self._model_path + self.version + self.pathSep
        self._model = joblib.load(current_model_path + 'version_' + self.version +'.pkl')
        print(current_model_path + 'features.dump')
        with open(current_model_path + 'features.dump','rb') as fp:
            self._features = pickle.load(fp)


    # predict results
    def Predict(self, df):
        df_predict = df[self._features]
        return self._model.predict(df_predict.values)


    # calculate turn sentiment
    def _calculate_turn_sentiment(self, row, df):
        pos_df = df[(df['turn'] == row['turn']) & (df['sentiment'] > 0)]
        neg_df = df[(df['turn'] == row['turn']) & (df['sentiment'] < 0)]
        neutral_df = df[(df['turn'] == row['turn']) & (df['sentiment'] == 0)]

        if pos_df.shape[0] > neg_df.shape[0]:
            if pos_df.shape[0] > neutral_df.shape[0]:
                row['sentiment'] = 1
            else:
                row['sentiment'] = 0
        else:
            if neg_df.shape[0] > neutral_df.shape[0]:
                row['sentiment'] = -1
            else:
                row['sentiment'] = 0

        return row


    # calculates results by turns
    def CalculateByTurns(self, df_sentiment, df_dialog):
        return df_dialog.apply(lambda row: self._calculate_turn_sentiment(row, df_sentiment), axis = 1)
