import csv
from tools.dialogs import person as personDialog

# this class handles list of turns in dialog
# the list of represented as lis ot Person objects
class Container(object):

	# constructor
	def __init__(self):
		self._list_people = None
		self._num_parts_justices = -1


	# setter for dialog
	def SetDialog(self, actDialog):
		self._dialog = actDialog
		self._list_people = None
		self._num_parts_justices = -1


	# returns the current dialog
	def GetDialog(self):
		return self._dialog


	def LoadFromFile(self, filename):
		self._dialog = []
		people = personDialog.Person()
		with open(filename, 'rb') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			skippedFirstLine = False
			readSentiment = False
			for row in reader:
				# skip header line
				if skippedFirstLine:
					obj = people.GetEmpty()
					obj['role'] = row[0]
					obj['name'] = row[1]
					obj['text'] = row[2]
					obj['was_interrupted'] = row[3] == '1'
					obj['turn'] = (int)(row[4])
					if readSentiment:
						obj['sentiment'] = row[5]
					self._dialog.append(obj)
				else:
					readSentiment = len(row) > 5
					skippedFirstLine = True
