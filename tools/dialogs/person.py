

# wrapper class representing one person
class Person(object):

	# creates an empty person for dialog
	def GetEmpty(self):
		return {
				'name' : '',
				'text' : '',
				'was_interrupted' : False,
				'role' : 'other',
				'turn' : 0
			}


	# creates an object for a person for reporting justices turns
	def GetEmptyReportTurns(self, parts, val):
		return {
				'role' : parts[0],
				'name' : parts[1],
				'turns' : val
		}


	# creates an object for a person for reporting who follows each justice and when
	def GetEmptyReportFollows(self, parts, followee, position):
		return {
				'role' : parts[0],
				'name' : parts[1],
				'follower' : '|'.join(parts),	# justice #2
				'followee' : followee, # justice #1
				'position' : position
		}


	# creates an object for a person for reporting justices turns
	def GetEmptyReportMostFollow(self, parts, val, follower):
		return {
				'role' : parts[0],
				'name' : parts[1],
				'follower' : follower,
				'ratio' : val
		}


	# creates an empty object for a person for reporting length and position of justices turns
	def GetEmptyReportTurnLength(self, parts, position, length, info):
		return {
				'role' : parts[0],
				'name' : parts[1],
				'position' : position,
				'length' : length,
				'information' : info
		}


	# creates an empty object for person with POS tags describing its text
	def GetEmptyPosPerson(self, name, turn, sent, sent_id, was_interrupted, role):
		return {
				'name' : name,
				'turn' : turn,
				'sentence' : sent,
				'sentence_id' : sent_id,
				'was_interrupted' : was_interrupted,
				'role' : role,
				'pos' : []
				}


	# creates an empty object for person with POS tags describing its text
	def GetEmptyNounsPerson(self, name, role, nouns):
		return {
				'name' : name,
				'role' : role,
				'nouns' : nouns
				}


	# creates an empty object for person to count words
	def GetEmptyCountWordsPerson(self, name, role, countWords, countTurns, wordsPerTurn):
		return {
				'name' : name,
				'role' : role,
				'words' : countWords,
				'turns' : countTurns,
				'wordsPerTurn' : wordsPerTurn
				}


	# creates an empty object for sentence in turn
	def GetEmptySentencePerson(self, name, turn, sent, sent_id, was_interrupted, role):
		return {
				'name' : name,
				'turn' : turn,
				'was_interrupted' : was_interrupted,
				'role' : role,
				'sentence' : sent,
				'sentence_id' : sent_id
				}

	# creates an empty record for sentiment of ona turn
	def GetPolarizedTurnsPerson(self, nameRole, count, sentiment ):
		data = nameRole.split('|')
		return {
				'name' : data[0],
				'role' : data[1],
				'polarized-class' : sentiment,
				'turns' : count
				}

	# creates an empty record for
	def GetEmptyQuestionPart(self, name, role):
		return {
			'name': name,
			'role': role,
			'turn': -1,
			'count': 0
		}
