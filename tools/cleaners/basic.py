from tools.filehelper import Filehelper
import re

# this class tries to clean up text parsed from PDF
class Basic:

	# constructor
	def __init__(self, outputDir):
		self.__outputDir = outputDir


	# cleaning up function - returns only transfript from oral argument
	def cleanUp(self, fileName):
		helper = Filehelper()
		newFileName = self.__outputDir + helper.GetFileName(fileName) + ".clean"

		actFile = open(fileName, 'r')
		outFile = open(newFileName, 'w+')
		firstPartDone = False	# checks, if the introduction part is done and arugment can be added to output file
		reProceedings = re.compile("P R O C E E D I N G S\s*\(\d{2}:\d{2}\s(a|p)\.m\.\)");
		reCaseSubmitted = re.compile("The case is submitted\.\s*\(Whereupon,");

		prevTwoLines = ['','']
		res = []
		for line in actFile:

			 # trim white spaces
			line = line.strip()
			if len(line) == 0: # skip empty lines
				continue

			# keep track of last 2 non-empty lines
			prevTwoLines[0] = prevTwoLines[1]
			prevTwoLines[1] = line
			actLine = ' '.join(prevTwoLines)

			# is this the beginning of proceeding?
			if reProceedings.search(actLine) != None:
				firstPartDone = True
				continue

			# check, if the case was submitted => end reading the file and do not write the previous line to clean file
			if reCaseSubmitted.search(actLine) != None:
				res.pop()
				break

			if firstPartDone:
				res.append(line + "\n")

		outFile.writelines(res) # write clean file