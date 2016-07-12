import controllers.base
from tools.parsers import largemoviereviews as largeMovieReviewsParser

class Largereviews(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'read-raw-corpus' : self._readRawCorpus
        }


    # method that reads raw corpus and transforms it into one coherent CSV file
    def _readRawCorpus(self):
        parser = largeMovieReviewsParser.LargeMovieReviews()
        data = parser.readFileRaw(None)
        parser.saveFileCsv(data, None)
