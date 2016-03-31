# Helper class for dialog containers
class Helper:

	# get list of people who participate in the dialog
	# returns list of arrays in form [0 => role, 1 => name]
	def GetListPeople(self, dialog, onlyJustices = False):
		listPeople = []
		# no information is cached so far, or refresh was requested
		for person in dialog:
			actPerson = person['role'] + "|" + person['name']
			if actPerson not in listPeople:
				listPeople.append(actPerson)

		listPeople = [p.split('|') for p in listPeople]


		# return list of justices, if asked for
		if onlyJustices:
			return [p for p in listPeople if p[0] == 'justice']
		else:
			return listPeople


	# this method gets number of dialog parts which belong to justices
	def CountJusticesParts(self, dialog):
		# calculate the number, if needed or requested
		return len([p for p in dialog if p['role'] == 'justice'])