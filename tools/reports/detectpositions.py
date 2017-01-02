import csv
import re
from tools.dialogs import person as personDialog
from tools.dialogs import helper as dialogHelper

# this class prepares reports from loaded dialog
# it expect list of Person objects
# REPORT Description:
# The report detects positions of people in the argument
class DetectPositions(object):

    # constructor
    def __init__(self, reportsDir):
        self.__outputDir = reportsDir
        self.__dialog = None


    # sets dialog for this report
    def SetDialog(self, newDialog):
        self.__dialog = newDialog


    # calculates longest turns per each justice
    def Detect(self):
        if self.__dialog == None:
            return None

        helper = dialogHelper.Helper()

        peopleHandler = personDialog.Person()
        people = helper.GetListPeople(self.__dialog.GetDialog(), False, True)
        reRespondent = re.compile("ON BEHALF OF (THE )?(STATE )?(UNION )?(INDUSTRY )?(AND )?(LOCAL )?(LABOR )?(PRIVATE )?"+
                                  "(FEDERAL )?(RESPONDENTS?|RESPONDENT BURROW|RESPONDENT FRANKS|APPELLEES?|UNITED STATES|FEDERAL GOVERNMENT|"+
                                  "INTERVENOR-RESPONDENTS IN SUPPORT OF THE PETITIONERS|INDUSTRY PETITIONERS AND RESPONDENTS IN SUPPORT)")
        reRespondent2 = re.compile("SUPPORTING (THE )?(the )?(RESPONDENTS?|APPELLEES?|AFFIRMANCE IN PART AND REVERSAL IN PART|JUDGMENT BELOW)")
        reRespondent3 = re.compile("(SUPPORTING VACATUR AND REMAND|IN SUPPORT OF THE JUDGMENT BELOW|SUPPORTING VACATUR)")
        rePetitioner = re.compile("ON BEHALF OF (THE )?(NO\. 14-614 )?(NO\. 14-623 )?(PRIVATE PARTY )?(STATE )?(FEDERAL )?(PRIVATE )?(PETITIONERS?|APPELLANTS?|PLAINTIFF|DEFENDANTS|PRIVATE PARTIES|COURT-APPOINTED AMICUS CURIAE)")
        rePetitioner2 = re.compile("SUPPORTING (THE )?(STATE )?(PETITIONERS?|APPELLANTS?|NEITHER PARTY)")
        res = []

        # walk through the dialog and calculate it
        previousPerson = None
        turn = 0
        parts = self.__dialog.GetDialog()
        for part in parts:
            if part['role'] != 'other':
                turn += 1
                continue

            actPerson = part['name']
            if actPerson != previousPerson:
                record = peopleHandler.GetEmptyPositionPerson(actPerson)
                actTurn = turn
                while turn - actTurn < 3:
                    record['turn'] = actTurn
                    if reRespondent.search(parts[actTurn]['text']) is not None or \
                       reRespondent2.search(parts[actTurn]['text']) is not None or \
                       reRespondent3.search(parts[actTurn]['text']) is not None:
                        record['position'] = 1
                        break
                    elif rePetitioner.search(parts[actTurn]['text']) is not None or \
                         rePetitioner2.search(parts[actTurn]['text']) is not None:
                        record['position'] = 0
                        break
                    actTurn -= 1

                if record['position'] != '':
                    res.append(record)

            previousPerson = actPerson
            turn += 1

        return sorted(res, key=lambda row: row['turn'])


    # this method saveds data produced by this report to a CSV file
    def SaveToFile(self, data, name = None):
        fileName = 'positions.csv'
        if name != None:
            fileName = name + ".csv"

        with open(self.__outputDir + fileName, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerow(['Name', 'Position', 'Turn'])
            for row in data:
                writer.writerow([row['name'], row['position'], row['turn']])
