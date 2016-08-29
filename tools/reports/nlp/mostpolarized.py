from tools.dialogs import person as personDialog
from tools.dialogs import helper as helperDialog


# this class prepares reports from loaded dialog
# REPORT Description:
# The report returns ordered list of justices by number of their sentiment polarized turns.
# There will be 3 separate list (positive turns, neutral turns, negative turns)
class MostPolarized(object):

    # constructor
    def __init__(self, reportsDir, pprint):
        self.__outputDir = reportsDir
        self.__dialog = None
        self.__pprint = pprint


    # sets dialog for this report
    def SetDialog(self, newDialog):
        self.__dialog = newDialog


    # sorting polarized data
    def __sort_polarized_counts(self, a, b):
        if a[2] < b[2]:
            return -1
        elif a[2] > b[2]:
            return 1
        else:
            if a[1] > b[1]:
                return 1
            elif a[1] < b[1]:
                return -1
            else:
                return 0


    # calculates polarized turns counts by justice and by polarization class
    def CalculatePolarizationCounts(self):
        helper = helperDialog.Helper()
        # prepare data structures
        peopleHelper = personDialog.Person()
        people = helper.GetListPeople(self.__dialog.GetDialog())
        data = { -1 : None, 0 : None, 1 : None }
        counts = {-1 : 0, 0 : 0, 1 : 0}
        for polarized_class in data.keys():
            data[polarized_class] = { justice[1]+"|"+justice[0] : 0 for justice in people }

        for turn in self.__dialog.GetDialog():
            data[(int)(turn['sentiment'])][turn['name']+"|"+turn['role']] += 1
            counts[(int)(turn['sentiment'])] += 1

        final_data = []
        for polarized_class in data.keys():
            for justice, calculated_data in zip(data[polarized_class].keys(), data[polarized_class].items()):
                final_data.append([justice, calculated_data[1], polarized_class])

        final_data.sort(self.__sort_polarized_counts, reverse = True)
        final_list_objects = []
        for line in final_data:
            final_list_objects.append(peopleHelper.GetPolarizedTurnsPerson(line[0], line[1], line[2]))
        self.__pprint.pprint(final_list_objects)
        self.__pprint.pprint(counts)
        return final_list_objects

    # saves the report to file
    def SaveToFile(self, data, name = None):
        fileName = 'most_polarized.csv'
        if name is not None:
            fileName = name + "_" + str(self.__threshold) + ".csv"

        with open(self.__outputDir + fileName, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            writer.writerow(['name', 'role', 'turns', 'polarized-class'])
            for record in data:
                writer.writerow([record['name'], record['role'], record['turns'], record['polarized-class']])
