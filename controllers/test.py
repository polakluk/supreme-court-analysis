import controllers.base

class Test(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'test' : self._test
        }


    # method for testing code and short experiments
    def _test(self):
        pass
