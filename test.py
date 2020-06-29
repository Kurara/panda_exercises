import unittest
import logging
import pandas as pd


class TestPandas(unittest.TestCase):

    def setUp(self):
        import os
        self.BASE_PATH = os.path.dirname(os.path.abspath(__file__))

    def test_csv_read(self):
        import time
        filepath = self.BASE_PATH + "/mockups/complaints.csv"
        start = time.time()
        df = pd.read_csv(filepath)
        print("Inserito csv dentro del DataFrame in {} secondi".format(
            time.time() - start
        ))
        print(df.head(7))



