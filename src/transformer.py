import pandas as pd


class Transformer:
    """
    This class is capable of transforming data from a pandas dataframe into a new pandas dataframe.
    """

    def __init__(self, df,  date_columns=None):
        self._df = df
        self.date_columns = date_columns

    def clean(self, dates=True, whitespace=True):
        if dates:
            self.standardise_dates()
        if whitespace:
            self.standardise_whitespace()
        return self._df.apply(lambda s: s.upper() if type(s) == str else s)

    def standardise_whitespace(self):
        self._df.apply(lambda w: w.replace(r"\s+", " ").strip() if type(w) == str else w)

    def standardise_dates(self):
        for col in self.date_columns:
            self._df[col] = pd.to_datetime(self._df[col], format="%d/%m/%Y")
