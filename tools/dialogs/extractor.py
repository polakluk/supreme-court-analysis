# -*- coding: utf-8 -*-

import re
import csv
from tools.dialogs import person as personDialog
from tools.filehelper import FileHelper

# this class receives cleaned text and extract
class Extractor(object):

	# constructor
	def __init__(self, outputDir, isDebug):
		self.__outputDir = outputDir
		self.__debug = isDebug


	# this method will extract parts of dialog per person
	# the function returns list of objects in format
	# {
	#    'person' : 'name of the person',
	#    'text' : 'what the person said',
	#    'was_interrupted' : 'true or false indicating whether this part of dialog was interruped by following speaker'
	#    'role' : 'either "justice" or "other" in dialog'
	#}
	def Extract(self, text):
		res = []

		people = personDialog.Person()
		reFindPeople = re.compile("(\n|--|^)(MR\s?\.\s?|JUSTICE|THE|CHIEF JUSTICE|GENERAL|MRS\s?\.\s?|MS\s?\.\s?)(\s\w+)+:")
		lastMessageEnded = 0 # position where the last person's part ended

		# these two variables take care of properly loading data
		# IDEA:
		# save information (name and role) to actPerson
		# if you are processing at least second person, go back to the previous person
		# add, wheter their part was interruped & the text itself
		# add the previous person to the final list
		# Usually, the last part in dialog is confirmation that the argument is over
		prevPerson = {}
		actPerson = None
		turn = 0
		for person in reFindPeople.finditer(text):
			#swap person
			prevPerson = actPerson

			# start a new person
			actPerson = people.GetEmpty()

			if person.group(2).replace(' ', '') == 'THE' and person.group(3).replace(' ', '') == 'COURT':
				actPerson['role'] = 'justice'
				actPerson['name'] = 'ROBERTS'
			else:
				actPerson['role'] = self._identifyRole(person.group(2).replace(' ', ''))
				actPerson['name'] = self.fixNames(person.group(3).replace(' ', ''), actPerson['role'])
				actPerson['turn'] = turn

				if actPerson['name'] == 'SCALIA':
					actPerson['role'] = 'justice'
				elif actPerson['name'] == 'BREYER':
					actPerson['role'] = 'justice'

			# if this is the first person to be processed,
			# set the marker to position AFTER peron's name
			if prevPerson != None:
				# ok, process this person
				txt = text[lastMessageEnded:person.start()].strip()

				if txt[-2:] == '--':
					prevPerson['was_interrupted'] = True
					prevPerson['text'] = self._clearTextPart( txt[:len(txt)-2] ) # use text without interruption marks
				else:
					prevPerson['text'] = self._clearTextPart( txt )

				if person.group(1).strip() == "--" : # yeah, the previous person was interrupted
					prevPerson['was_interrupted'] = True

				res.append(prevPerson)


			lastMessageEnded = person.end() + 1
			turn += 1

		actPerson['text'] = self._clearTextPart( text[lastMessageEnded:] )
		res.append(actPerson)
		if self.__debug == True:
			for row in res:
				print(row)

		return res


	# selects the corret for for person
	def _identifyRole(self, role):
		if role == 'JUSTICE' or role == 'CHIEFJUSTICE':
			return 'justice'
		return 'other'


	@classmethod
	def fixNames(cls, name, role):
	    mapping = {
	    	'other': {    	
		        'McCarthy': 'MCCARTHY',
		        'McCARTHY': 'MCCARTHY',
		        'MITCIELL': 'MITCHELL',
		        'MITCiELL': 'MITCHELL',
				'McGILL': 'MCGILL',
		        'McALLISTER': 'MCALLISTER',
		        'THIEKMAN': 'THIERMAN',
		        'THEIRMAN': 'THIERMAN',
		        'McCRACKEN': 'MCCRACKEN',
		        'FISCHER': 'FISHER',
				'FISHEQ': 'FISHER',
		        'GOLDBERG': 'GOLDENBERG',
		        'PHILIPS': 'PHILLIPS',
				'DREESEN': 'DREEBEN',
				'FELDWAN': 'FELDMAN',
		        'HANSMEIEQ': 'HANSMEIER',
		        'ANDEQS': 'ANDERS',
		        'H0': 'HO',
		        'RUSSEL': 'RUSSELL',
		        'DeSANCTIS': 'DESANCTIS',
		        'DREE3EN': 'DREEBEN',
		        'LYNCi': 'LYNCH',
		        'HACKEQ': 'HACKER',
		        'McCONNELL': 'MCCONNELL',
		        'GOLDSLATT': 'GOLDBLATT',
				'KS': 'ANDERS',
	    	},
	    	'justice': {
		       'RO3ERTS': 'ROBERTS',
		       '3REYER': 'BREYER',
		       'BQEYER' : 'BREYER',
		       'SREYER': 'BREYER',
		       'SREYER': 'BREYER',
		       'SOTOMAYOQ': 'SOTOMAYOR',
		       'ROSERTS': 'ROBERTS',
		       'SOTOWAYOR': 'SOTOMAYOR',
		       'SOTOMAYOK': 'SOTOMAYOR',
		       'GINSBERG': 'GINSBURG',
		        'KENNEY': 'KENNEDY',
		        'SCLIA': 'SCALIA',
	    	}
	    }
	    if name in mapping[role].keys():
	        return mapping[role][name]
	    return name



	# this method cleans up text part for each person so any preceeding -- will be removed
	def _clearTextPart(self, text):
		res = text.replace("\n", ' ').strip()
		if res[:2] == '--':
			return res[2:].strip()
		else:
			return res


	# this method saveds data produced by this report to a CSV file
	def SaveToFile(self, data, name = None):
		helper = FileHelper()
		fileName = helper.GetFileName(name) + ".dialog"

		with open(self.__outputDir + fileName, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			writer.writerow(['role', 'name', 'text', 'was interrupted', 'turn'])
			for row in data:
				was_interrupted = '0'
				if row['was_interrupted']:
					was_interrupted = '1'
				writer.writerow([row['role'], row['name'], row['text'], was_interrupted, row['turn']])
