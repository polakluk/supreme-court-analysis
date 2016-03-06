

# this class handles list of turns in dialog
# the list of represented as lis ot Person objects
class Container:

	# constructor
	def __init__(self):
		self.__list_people = None


	# setter for dialog
	def SetDialog(self, actDialog):
		self.__dialog = actDialog
		self.__list_people = None
		self.__num_parts_justices = -1


	# returns the current dialog
	def GetDialog(self):
		return self.__dialog


	# get list of people who participate in the dialog
	# returns list of arrays in form [0 => role, 1 => name]
	def GetListPeople(self, onlyJustices = False, refresh = False):
		if self.__dialog == None: # no dialog defined yet
			return []

		# no information is cached so far, or refresh was requested
		if self.__list_people == None or refresh:
			self.__list_people = []
			for person in self.__dialog:
				if onlyJustices and person['role'] != 'justice':
					continue

				actPerson = person['role'] + "|" + person['name']
				if actPerson not in self.__list_people:
					self.__list_people.append(actPerson)

			self.__list_people = [p.split('|') for p in self.__list_people]


		return self.__list_people

	# this method gets number of dialog parts which belong to justices
	def CountJusticesParts(self, refresh = False):
		# calculate the number, if needed or requested
		if self.__num_parts_justices == -1 or refresh:
			self.__num_parts_justices = len([p for p in self.__dialog if p['role'] == 'justice'])

		return self.__num_parts_justices