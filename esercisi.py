import unittest
import logging
import pandas as pd
import numpy as np


class TestPandas(unittest.TestCase):

    # Mettere insieme latitude and longitude in same column
    # Lista dei 'descript' per weekdays
    # Multiindex warrants/warrnts arrest
    # Tabella pivote
    def setUp(self):
        import os
        self.BASE_PATH = os.path.dirname(os.path.abspath(__file__))
        self.sf_filepath = self.BASE_PATH + "/mockups/train.csv"
        self.sanfrancisco_df = pd.read_csv(self.sf_filepath)
        self.sanfrancisco_df['Dates'] = self.sanfrancisco_df['Dates'].map(self.str_to_date)

    def str_to_date(self, str_date):
            #2020-01-17
        new_date = str_date
        if str_date is not None and len(str_date) > 0:
            date_parts = str_date.split(' ')
            data = date_parts[0].split('-')
            hours = date_parts[1].split(':')
            new_date = pd.Timestamp(year=int(data[0]), month=int(data[1]), day=int(data[2]))
        return new_date

    def join_lon_lat(self, row):
        row['Position'] = '({}, {})'.format(row['X'], row['Y'])

        return row

    def test_unire_colonne(self):
        self.sanfrancisco_df['Position'] = self.sanfrancisco_df['X']
        self.sanfrancisco_df.apply(self.join_lon_lat, axis=1)
        print("Con la nuova colonna:\n", sanfrancisco_df)

        self.sanfrancisco_df.drop_column(['X', 'Y'], axis=1)
        print("Risultato:\n", sanfrancisco_df)

    def test_crime_piu_comune(self):
        most_common = self.sanfrancisco_df.groupby(['Category', 'Descript'])['Category'].count()
        print(most_common.sort_values(ascending=False).head(1))

    def test_crimine_per_distritto(self):
        pass

    def test_pivotte(self):
        filepath = self.BASE_PATH + "/mockups/train.csv"
        sanfrancisco_df = pd.read_csv(filepath)

        grouped = sanfrancisco_df.groupby(['Category', 'DayOfWeek']).Category.count()
        print(grouped)
        pivote = sanfrancisco_df.pivot_table(sanfrancisco_df, index=['Category'],
                    columns=['DayOfWeek'], aggfunc='count')  
        print(pivote)
        print(pivote['Address'])
        print(pivote.transpose().info())
        transposed = pivote.transpose().droplevel(0)
        transposed.drop_duplicates(inplace=True)
        new_pivote = transposed.transpose()
        print(new_pivote)

    
