# needed
import pprint
import argparse
import importlib

# This is a controller class that handles execution of all tasks in this project
class Controller(object):

    # controller
    def __init__(self, isDebug, timeIt):
        self.isDebug = isDebug
    	self.pprint = pprint.PrettyPrinter(indent = 4 )
        self.timeIt = timeIt
        self.argParser = None


    def _initializeArgumentParser(self):
        self.argParser = argparse.ArgumentParser(description='Analytic tool for Supreme Court Oral Argument', add_help = False)
        self.argParser.add_argument('-c', help="Controller name", dest="controller", required=True)
        self.argParser.add_argument('-t', help="Task name ('help' will print argument parser help for the controller)", dest="task", required=True)


    # entry point for code execution
    def Execute(self):
        # initialize the argument parser only once
        if self.argParser == None:
            self._initializeArgumentParser()

        args = self.argParser.parse_known_args()[0]
        # prevent user from initializing base controller
        if args.controller == 'base':
            self.pprint.pprint("You cannot initialize Base controller")
            return

        className = "controllers."+args.controller
        try:
            moduleClass = getattr(importlib.import_module(className), args.controller.title())
            controller = moduleClass(self.pprint, self.argParser)
            controller.SetDebug(self.isDebug)
            controller.SetTimeIt(self.timeIt)
            controller.Execute()
        except ImportError as e:
            self.pprint.pprint("No controller found")
