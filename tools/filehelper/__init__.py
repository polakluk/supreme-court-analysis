import os


class FileHelper:
	def GetFileName(self, file):
		path = file.split(os.path.sep)
		fileNameParts = path[-1].split('.')

		return '.'.join(fileNameParts[0:(len(fileNameParts) - 1 )])