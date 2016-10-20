import controllers.base
from tools.parsers.corpuses_sentiment import largemoviereviews as largeMovieReviewsParser

class Largereviews(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'read-raw-corpus' : self._readRawCorpus,
                                'read-raw-corpus-overall' : self._readRawCorpusOverall
        }


    # method that reads raw corpus and transforms it into one coherent CSV file
    def _readRawCorpus(self):
        parser = largeMovieReviewsParser.LargeMovieReviews()
        data = parser.readFileRaw(None)
        parser.saveFileCsv(data, None)

    # method that reads raw corpus and saves only information about id, rating and sentiment of each review
    def _readRawCorpusOverall(self):
        parser = largeMovieReviewsParser.LargeMovieReviews()
        data = parser.readFileOverallData(None)
        parser.saveFileCsv(data, parser.defaultFileNameProcessedOverall)
