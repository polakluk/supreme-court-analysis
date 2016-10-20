import controllers.base
import re
from tools.filehelper import FileHelper

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
        helper = FileHelper()
        fNameRaw = helper.GetFileName('.\arguments\modes.info')
        print fNameRaw
