# needed
import os
import sys
import getopt
import controller as mainController

# main
def main(argv):

	mode = (int)(argv[1])
	controller = mainController.Controller(True, True)

	if len(argv) > 3: # was specified custom output directory
		controller.Execute(mode, argv[2], argv[3])
	else: # no, so use the default
		controller.Execute(mode, argv[2])
	return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
