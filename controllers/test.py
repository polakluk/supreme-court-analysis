import controllers.base
import re
from tools.parsers import negation as negationParser

class Test(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'test' : self._test
        }


    # method for testing code and short experiments
    def _test(self):
#        parser = negationParser.Negation()
#        data = parser.readFileRaw(None)
#        parser.saveFileCsv(data, None)
#        print(data)
        print "Test script"
