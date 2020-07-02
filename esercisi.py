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
        # Questa funziona sotto dovrebbe funzionare ma non crea la colonna
        # self.sanfrancisco_df.assign(Position=lambda df: '({}, {})'.format(df.X, df.Y), inplace=True)
        print("Con la nuova colonna:\n", self.sanfrancisco_df)

        self.sanfrancisco_df.drop(['X', 'Y'], axis=1)
        print("Risultato:\n", self.sanfrancisco_df)

    def test_crime_piu_comune(self):
        most_common = self.sanfrancisco_df.groupby(['Category', 'Descript'])['Category'].count()
        print(most_common.sort_values(ascending=False).head(1))

    def test_crimine_per_distritto(self):
        pass

    def test_pivotte(self):
        #giorno piu crimini
        grouped = self.sanfrancisco_df.groupby(['DayOfWeek']).Category.count().sort_values(ascending=False)
        print(grouped)
        #altro
        pivote = self.sanfrancisco_df.pivot_table(self.sanfrancisco_df, index=['Category'],
                    columns=['DayOfWeek'], aggfunc='count')  
        print(pivote)
        print(pivote['Address'])
        print(pivote.transpose().info())
        transposed = pivote.transpose().droplevel(0)
        transposed.drop_duplicates(inplace=True)
        new_pivote = transposed.transpose()
        print(new_pivote)

    def test_multindex(self):
        pivote_multi_index = self.sanfrancisco_df.pivot_table(
            self.sanfrancisco_df, index=['Category', 'Descript'], aggfunc='max'
        )
        print(pivote_multi_index)

    def test_crimine_piu_arresti(self):
        import matplotlib.pyplot as plt

        print(self.sanfrancisco_df.groupby('Resolution').count()['Category'])

        pivote_crimini_arresti = self.sanfrancisco_df.pivot_table(
            self.sanfrancisco_df, index=['Category', 'Descript'], columns='Resolution', aggfunc='count'
        )
        print(pivote_crimini_arresti)
        uni_index_pivote = pivote_crimini_arresti['Address'].sort_values(by=['ARREST, BOOKED', 'ARREST, CITED'], ascending=False)
        print("Tabella finale:\n", uni_index_pivote)   

        uni_index_pivote.plot() 

        plt.show()
