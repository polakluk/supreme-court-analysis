import csv
from tools.dialogs import person as personDialog

# this class handles list of turns in dialog
# the list of represented as lis ot Person objects
class Container(object):

	# constructor
	def __init__(self):
		self.__list_people = None
		self.__num_parts_justices = -1


	# setter for dialog
	def SetDialog(self, actDialog):
		self.__dialog = actDialog
		self.__list_people = None
		self.__num_parts_justices = -1


	# returns the current dialog
	def GetDialog(self):
		return self.__dialog


	def LoadFromFile(self, filename):
		self.__dialog = []
		people = personDialog.Person()
		with open(filename, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			skippedFirstLine = False
			for row in reader:
				# skip header line
				if skippedFirstLine:
					obj = people.GetEmpty()
					obj['role'] = row[0]
					obj['name'] = row[1]
					obj['text'] = row[2]
					obj['was_interrupted'] = row[3] == '1'
					self.__dialog.append(obj)
				else:
					skippedFirstLine = True
