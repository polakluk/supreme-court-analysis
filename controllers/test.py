import controllers.base
import re

class Test(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'test' : self._test
        }


    # method for testing code and short experiments
    def _test(self):
        testText = """He
                proposed inserting CIA teams into Afghanistan to work with Afghan warlords who would
                join the fight against al Qaeda."""

        print(testText)
        print(re.sub('\s+', ' ', testText))
