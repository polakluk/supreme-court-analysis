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
        line = '1394	56,94	string	GATE_direct-subjective	 expression-intensity="neutral" insubstantial="C2" intensity="medium" nested-source="w, implicit" polarity="" attitude-link="greatAccomplish" '
        pos = line.find('polarity="')
        lenPolarity = len('polarity="')
        print(line[pos+lenPolarity:]) 
