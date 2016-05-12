import time
import os
import argparse

# base controller for all subcontrollers
class Base(object):
    # constructor
    def __init__(self, pprinter, argParse ):
        self.timeit = False
        self.debug = False
        self.timeIt = False
        self.pprint =  pprinter
        self.pathSeparator = os.path.sep
        self.parsedDataDir = "."+self.pathSeparator+"parsed-data"+self.pathSeparator
        self.reportDataDir = "."+self.pathSeparator+"report-data"+self.pathSeparator
        self.corporaDir = "."+self.pathSeparator+"corpora"+self.pathSeparator
        self.availableTask = {}
        self.parentArgParse = argparse
        self.argParser = argparse.ArgumentParser(parents = [argParse])
        self.parserInitialized = False


    # sets debuging info
    def SetDebug(self, debug):
        self.debug = debug


    # sets timing flag
    def SetTimeIt(self, timeit):
        self.timeIt = timeit


    # initializes its own parser
    def initializeArgumentParser(self):
        pass


    # executes task selected in command line
    def Execute(self):
        if self.parserInitialized == False:
            self.initializeArgumentParser()
        args = self.argParser.parse_args()
        taskName = args.task
        if self.debug:
            self.pprint.pprint("Task name: " + taskName)
        timeStart = timeEnd = 0

        if self.timeIt:
            tStart = time.time()

        if taskName == 'help': # hard-coded shortcut for printing help for command-line arguments
            self._printHelp()
        else:
            if taskName in self.availableTask.keys():
                self.availableTask[taskName]()
            elif self.debug:
                self.pprint.pprint("Task '" + taskName + "' was not found")

        if self.timeIt:
            tEnd = time.time()
            print "Elapsed time: " + str(tEnd - tStart)


    def _printHelp(self):
        self.argParser.print_help()
