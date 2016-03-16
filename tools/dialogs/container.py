import csv
from tools.dialogs import person as personDialog

# this class handles list of turns in dialog
# the list of represented as lis ot Person objects
class Container:

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


	# get list of people who participate in the dialog
	# returns list of arrays in form [0 => role, 1 => name]
	def GetListPeople(self, onlyJustices = False, refresh = False):
		if self.__dialog == None: # no dialog defined yet
			return []

		# no information is cached so far, or refresh was requested
		if self.__list_people == None or refresh:
			self.__list_people = []
			for person in self.__dialog:
				actPerson = person['role'] + "|" + person['name']
				if actPerson not in self.__list_people:
					self.__list_people.append(actPerson)

			self.__list_people = [p.split('|') for p in self.__list_people]


		# return list of justices, if asked for
		if onlyJustices:
			return [p for p in self.__list_people if p[0] == 'justice']
		else:
			return self.__list_people


	# this method gets number of dialog parts which belong to justices
	def CountJusticesParts(self, refresh = False):
		# calculate the number, if needed or requested
		if self.__num_parts_justices == -1 or refresh:
			self.__num_parts_justices = len([p for p in self.__dialog if p['role'] == 'justice'])

		return self.__num_parts_justices