

# wrapper class representing one person
class Person:

	# creates an empty person for dialog
	def GetEmpty(self):
		return {
				'name' : '',
				'text' : '',
				'was_interruped' : False,
				'role' : 'other'
			}


	# creates an empty object for a person for reporting justices turns
	def GetEmptyReportTurns(self, parts, val):
		return {
				'role' : parts[0],
				'name' : parts[1],
				'turns' : val 
		}

	# creates an empty object for a person for reporting who follows each justice and when
	def GetEmptyReportFollows(self, parts, followee, position):
		return {
				'role' : parts[0],
				'name' : parts[1],
				'follower' : '|'.join(parts),	# justice #2
				'followee' : followee, # justice #1
				'position' : position
		}

	# creates an empty object for a person for reporting justices turns
	def GetEmptyReportMostFollow(self, parts, val, follower):
		return {
				'role' : parts[0],
				'name' : parts[1],
				'follower' : follower,
				'ratio' : val
		}
