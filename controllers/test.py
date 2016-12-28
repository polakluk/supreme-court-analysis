import controllers.base
from tools.pos import textblobpostagger as textBlobPosTagger

class Test(controllers.base.Base):

    # constructor
    def __init__(self, pprinter, argParse):
        controllers.base.Base.__init__(self, pprinter, argParse)
        self.availableTask = {
                                'test' : self._test
        }


    # method for testing code and short experiments
    def _test(self):
        text = 'Right. And I completely understand that, Mr Gannon, but even your own interpretation doesn\'t get you the information -- (Laughter.) (Lights out.)'
        pos = textBlobPosTagger.TextBlobPosTagger()

        print(pos.SeparateSentenctes(text))
