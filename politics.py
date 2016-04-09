# needed
import os
import sys
import getopt
import controller as mainController

# main
def main(argv):

	mode = (int)(argv[1])
	controller = mainController.Controller(True)
	controller.Execute(mode, argv[2])
	return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
