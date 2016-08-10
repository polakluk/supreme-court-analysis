from tools.parsers import basecorpus
from tools.text import sentencewords

import numpy as np
import pandas as pd
from os import walk
import nltk.data

# this class reads Large Movie Rviews corpus and turns it into a proper CSV file
# it reads both test and train sets and merges them into one CSV file (each row contains a flag saying to which set it belongs)
class LargeMovieReviews(basecorpus.BaseCorpus):
    # constructor
    def __init__(self):
        basecorpus.BaseCorpus.__init__(self)
        self.defaultDirNameOrig = '.'+self.sepDir+'corpora'+self.sepDir+'large-movie-review'+self.sepDir
        self.defaultFileNameProcessed = '.'+self.sepDir+'corpora'+self.sepDir+'processed'+self.sepDir+'large-movie-review.csv'
        self.defaultFileNameProcessedOverall = '.'+self.sepDir+'corpora'+self.sepDir+'processed'+self.sepDir+'large-movie-review-overall.csv'
        self._dataFrameColumns = ['id', 'rating', 'type', 'text', 'set']
        self._dataFrameColumnsOverall = ['id', 'rating', 'type', 'set']
        self._tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


    # gets list of all sentenes from all reviews in the set
    # set containts positive and negative reviews
    # result is a dataframe
    def _getListSentencesSource(self, source):
        sentences = pd.DataFrame({}, self._dataFrameColumns)
        types_reviews = {'neg' : -1, 'pos' : 1}
        for idx in types_reviews.keys():
            for (dirpath, dirnames, filenames) in walk(source+idx+self.sepDir):
                # go through all files
                for fname in filenames:
                    meta_data = fname.split('_')

                    current_sentences = self._parseFile(dirpath+fname)
                    if len(current_sentences) > 0:
                        current_frame = pd.DataFrame(np.zeros((len(current_sentences), len(self._dataFrameColumns))), columns = self._dataFrameColumns)
                        current_frame['text'] = current_sentences
                        current_frame['text'] = current_frame['text'].map(lambda cell: '|'.join(cell))
                        current_frame['id'] = meta_data[0]
                        current_frame['rating'] = meta_data[1].split('.')[0]
                        current_frame['type'] = types_reviews[idx]
                        current_frame['set'] = 1 if source[-6:] == 'train\\' else 0

                        sentences = sentences.append(current_frame, ignore_index = True)

        return sentences

    # gets list of all all reviews with their data
    # result is a dataframe
    def _getOverallDataSource(self, source):
        overallData = pd.DataFrame({}, columns = self._dataFrameColumnsOverall)
        types_reviews = {'neg' : -1, 'pos' : 1}
        for idx in types_reviews.keys():
            for (dirpath, dirnames, filenames) in walk(source+idx+self.sepDir):
                # go through all files
                for fname in filenames:
                    meta_data = fname.split('_')
                    df = pd.DataFrame(np.zeros((1, len(self._dataFrameColumnsOverall))), columns = self._dataFrameColumnsOverall)
                    df['id'] = meta_data[0]
                    df['rating'] = meta_data[1].split('.')[0]
                    df['type'] = types_reviews[idx]
                    df['set'] = 1 if source[-6:] == 'train\\' else 0
                    overallData = overallData.append(df, ignore_index = True)

        return overallData


    # open the file and get all sentences
    def _parseFile(self, sourceFile):
        with open(sourceFile, 'rb') as review_file:
            review = review_file.read()
            sentences = sentencewords.SentenceWords.review_to_sentences(review, self._tokenizer)
            return sentences


    # reads each  file and returns pandas DataFrame
    def readFileRaw(self, dirNameRaw):
        if dirNameRaw == None:
            dirName = self.defaultDirNameOrig

        review_sources = [dirName + 'train' + self.sepDir, dirName + 'test' + self.sepDir]

        reviews = pd.DataFrame({}, columns = self._dataFrameColumns)
        for directory in review_sources:
            reviews_read = self._getListSentencesSource(directory)
            reviews = reviews.append(reviews_read, ignore_index=True)

        return reviews


    # reads names of each file and returns pandas DataFrame
    def readFileOverallData(self, dirNameRaw):
        if dirNameRaw == None:
            dirName = self.defaultDirNameOrig

        review_sources = [dirName + 'train' + self.sepDir, dirName + 'test' + self.sepDir]

        reviews = pd.DataFrame({}, columns = self._dataFrameColumnsOverall)
        for directory in review_sources:
            reviews_read = self._getOverallDataSource(directory)
            reviews = reviews.append(reviews_read, ignore_index=True)

        return reviews
