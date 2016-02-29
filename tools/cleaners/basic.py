from tools.filehelper import Filehelper

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

		res = []
		totalLines = 0;
		for line in actFile:
			print
			totalLines += 1
			parts = line.strip().split()
			print '"'+line+'"'+str(len(line))
			print "Parts = " + str(len(parts)) + " ===== > " + str(totalLines)
			if( len(parts ) == 1 ): # tehre is only one "word" so there's a suspicion that it is only number of line
				try:
					num  = (int)(parts[0].strip())
					print( "Line " + str(totalLines) + " skipped #Exception#")
					continue
				except ValueError:
					# the value is OK => there is some text
					res.append(line)

			else:
				if len( parts ) == 0: # skip empty lines
					print( "Line " + str(totalLines) + " skipped #Empty Line#")
					continue;
				else:
					res.append(line)

		print( totalLines )
		print( len(res))
		outFile.writelines(res[:50])