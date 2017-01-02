# Helper class for dialog containers
class Helper(object):

	# get list of people who participate in the dialog
	# returns list of arrays in form [0 => role, 1 => name]
	def GetListPeople(self, dialog, onlyJustices = False, onlyOthers = False):
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
			if onlyOthers:
				return [p for p in listPeople if p[0] == 'other']				
			else:
				return listPeople


	# this method gets number of dialog parts which belong to justices
	def CountJusticesParts(self, dialog):
		# calculate the number, if needed or requested
		return len([p for p in dialog if p['role'] == 'justice'])


	# this method assigns position in dialog to each part
	def AssignPositionsPartsDialog(self, dialog):
		length = float(len(dialog))
		lenJustices = float(self.CountJusticesParts(dialog))
		idx = 0
		idxJustice = 0
		for part in dialog:
			part['positions'] = {'dialog' : 0, 'justice' : 0}
			part['positions']['dialog'] = idx / length
			idx += 1
			if part['role'] == 'justice':
				part['positions']['justice'] = idxJustice / lenJustices
				idxJustice += 1

		return dialog
