import pandas as pd


class LfCsvHelper:
    def __init__(self):
        self.df = pd.read_csv('coordinates/final_coordinates.csv')

    def get_words_by_category(self, category):
        return self.df['word'].where(self.df['category'] == category).unique().tolist()

    def get_categories(self):
        return self.df['category'].unique().tolist()

    def get_all_words(self):
        return self.df['word'].tolist()
