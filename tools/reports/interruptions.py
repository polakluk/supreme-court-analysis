import csv
import pandas as pd
from tools.dialogs import person as personDialog
from tools.dialogs import helper as dialogHelper

# this class prepares reports from loaded dialog
# it expect list of Person objects
# REPORT Description:
# The report counts interruptions by justice
class Interruptions(object):

    # constructor
    def __init__(self, reportsDir):
        self.__outputDir = reportsDir
        self.__dialog = None


    # sets dialog for this report
    def SetDialog(self, newDialog):
        self.__dialog = newDialog


    # calculates longest turns per each justice
    def CountInterruptions(self, dfPositions):
        if self.__dialog == None:
            return None

        helper = dialogHelper.Helper()

        peopleHandler = personDialog.Person()
        people = helper.GetListPeople(self.__dialog.GetDialog())

        res = {}

        actPhase = ''
        # walk through the dialog and calculate it
        dfPositions = [[record['turn'], record['name'], record['position']] for record in dfPositions]
        df = pd.DataFrame(dfPositions, columns=['Turn', 'Name', 'Position'])
        for part in self.__dialog.GetDialog():
            if df[df['Turn'] == int(part['turn'])].shape[0] > 0:
                actPhase = df[df['Turn'] == int(part['turn'])]['Position'].values[0]
            if part['was_interrupted'] and part['role'] == 'other':
                key = '{}-{}'.format(part['name'], actPhase)
                if key not in res:
                    res[key] = peopleHandler.GetEmptyInterruptionPerson(part['name'])

                res[key]['count'] += 1
                res[key]['position'] = actPhase

        res = sorted(res.values(), key = lambda x: x['count'], reverse = True)
        return res


    # this method saveds data produced by this report to a CSV file
    def SaveToFile(self, data, name = None):
        fileName = 'interruptions.csv'
        if name != None:
            fileName = name + ".csv"

        with open(self.__outputDir + fileName, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerow(['Name', 'Count', 'Position'])
            for row in data:
                writer.writerow([row['name'], row['count'], row['position']])
