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
        self.version = '5' # active version of sentiment model
        self.pathSep = os.path.sep
        self._model_path = '.'+self.pathSep + 'models-sentiment' + self.pathSep
        self._model = None
        self._features = []


    # loads current version of model
    def LoadModel(self):
        current_model_path = self._model_path + self.version + self.pathSep
        self._model = joblib.load(current_model_path + 'version_' + self.version +'.pkl')
        with open(current_model_path + 'features.dump','wb') as fp:
            self._features = pickle.load(fp)


    # predict results
    def Predict(self, df):
        df_predict = df[self._features]
        return self._model.predict(df_predict.values)
