import pandas as pd

class Merger(object):

    # constructor
    def __init__(self):
        self._dataframes = []
        pass


    def add_dataframe(self, df):
        self._dataframes.append(df)


    def export_dataframe(self, outputFile):

        if len(self._dataframes) == 0:
            return

        final_df = pd.DataFrame([], columns=self._dataframes[0].columns)
        for df in self._dataframes:
            final_df = pd.concat([final_df, df], ignore_index=True)

        final_df.to_csv(outputFile, index=False)
