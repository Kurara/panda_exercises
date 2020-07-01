import unittest
import logging
import pandas as pd
import numpy as np


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

    def test_series(self):
        lista = [2, 4, 6, 6]
        series = pd.Series(data=lista, index=['A', 'B', 'C', 'D'])

        print(series)

    def test_df_sostituzione(self):
        numpy_array = np.random.randn(5,4)
        df = pd.DataFrame(
            data=numpy_array,
            index=['valore1', 'valore2', 'valore3', 'valore4', 'valore5'],
            columns=['A', 'B', 'C', 'D'])
        print(df)
        print('\n')
        
        frutti = ['Anguria', 'Pompelmo', 'Fragole', 'Nespole', 'Lamponi']
        df['B'] = frutti
        print(df)
        print('\n')

    def test_eliminazione(self):
        numpy_array = np.random.randn(5,4)
        df = pd.DataFrame(
            data=numpy_array,
            index=['valore1', 'valore2', 'valore3', 'valore4', 'valore5'],
            columns=['A', 'B', 'C', 'D'])

        new_df = df.drop('A', axis=1)
        print("Vecchio senza inplace:\n", df)
        print("Nuovo senza inplace:\n",new_df)

        new_df = df.drop('A', axis=1, inplace=True)
        print("Vecchio con inplace:\n", df)
        print("Nuovo con inplace:\n",new_df)
        print("\n")

        new_df = df.drop('valore4', axis=0)
        print(new_df)

        # Se rinominiano le rige/colonne non possiamo più usare gli index
        with self.assertRaises(Exception):
            new_df = df.drop(0, axis=0)
            print(new_df)

    def test_selezione(self):
        numpy_array = np.random.randn(5,4)
        df = pd.DataFrame(
            data=numpy_array,
            index=['valore1', 'valore2', 'valore3', 'valore4', 'valore5'],
            columns=['A', 'B', 'C', 'D'])

        # Selezione righe
        # Selezione colonne
        # Selezione righe e colonne
        new_df = df[['A', 'B']].loc['valore2': 'valore4']
        print("Righe con nome:\n", new_df)

        new_df = df[['A', 'B']].iloc[2: 5]
        print("Righe con index:\n", new_df)

        positivi = df[df['A'] > 0]
        print("Valore 'A' positivo:\n", positivi)

        alt = df[(df['A'] > 0) & (df['B'] < 0)]
        print("Valore 'A' positivo e 'B' negativo:\n", alt)

    def test_colonne_col_tipo(self):
        frutti = ['Anguria', 'Pompelmo', 'Fragole', 'Nespole', 'Lamponi', 'Pesca', 'Melone', 'More']
        calorie = pd.Series([16, 26, 27, 28, 34, 27, 33, 36])
        colore = pd.Series(
            ['rosso', 'rosa', 'rosso', 'arancione', 'rosso', 'arancione', 'arancione', 'nero'],
            dtype=pd.StringDtype()
        )

        df = pd.DataFrame(
            data={
                'frutti': frutti,
                'calorie': calorie,
                'colore': colore,
            })

        print(df.info())

    def test_nulli(self):
        s = pd.Series([1,4,np.nan,2,None,5,6,8])
        print(s.isnull())
        print('\n')

        dew_df = s.dropna()
        print("Vuoti fuori:\n", dew_df)
        print('\n')

        dew_df = s.fillna(5)
        print("Riempita con 5:\n", dew_df)
        print('\n')

        # Essiste anche ffill
        print('Prima:\n', s)
        dew_df = s.fillna(method='bfill')
        print("Dopo:\n", dew_df)

    def test_concatenazione(self):
        import datetime
        clienti = pd.Series(['paco', 'vittoria', 'francesco'], dtype=pd.StringDtype())
        indirizzi = [np.nan, 'via 1', 'piaza 2']
        eta = [16, 56, 98]
        clienti_df = pd.DataFrame({
            'cliente': clienti,
            'indirizzo': indirizzi,
            'eta': eta
        })
        nome = ['uno', 'altro', 'non so'] 
        data = [datetime.datetime.now(), datetime.datetime.now(), datetime.datetime(year=2020, month=3, day=23)]
        motivi_df = pd.DataFrame({
            'nome': nome,
            'data': data,
            'usuario': clienti
        })

        df_col = pd.concat([motivi_df, clienti_df], axis=1)
        print("Axis1: \n", df_col)

        df_row = pd.concat([motivi_df, clienti_df], axis=0)
        print("Axis0: \n", df_row)

        print(
            "merge per i clienti/usuari:\n",
            pd.merge(clienti_df, motivi_df, left_on='cliente', right_on='usuario', left_index=True)
        )

        print(
            "join:\n",
            clienti_df.join(motivi_df)
        )

    def test_da_htm_div(self):
        # Per usare read_html bisogna installare la classe che legge gli xml/html "pip install lxml"
        list_corona_df = pd.read_html('https://statistichecoronavirus.it/')
        print(len(list_corona_df))
        for corona in list_corona_df:
            print(corona.head())

    def test_masivi(self):
        filepath = self.BASE_PATH + "/mockups/complaints.csv"
        df = pd.read_csv(filepath)

        print("Soltanto colonna Product:\n", df['Product'])
        print('\n')
        # print("Soltanto colonna Product unique:\n", df[df['Product'].unique()])
        # print('\n')
        print("Info:\n", df.info())
        print('\n')
        valori_nulli = df[df['Sub-issue'].isnull()]
        print("Tutti dati:\n", df.count())
        print("Dati con colonne nulle:\n", valori_nulli.count())
        print("Describe:\n", df['ZIP code'].describe())
        print("Describe:\n", df['Complaint ID'].describe())
        print("Soltanto colonna Product count:\n", df['Product'].value_counts())
        print('\n')

    def test_velocita_con_database(self):
        """ Selezioniamo la lista dei numeri di Sottoprodotto/Sub-product
        per il prodotto/Product 'Mortgage'

        """
        import time
        from mariadb import MariaDBManagement
        filepath = self.BASE_PATH + "/mockups/complaints.csv"
        df = pd.read_csv(filepath)
        
        start = time.time()
        sotto_prodotti = df[df['Product']=='Mortgage']['Sub-product']
        print(sotto_prodotti)
        print("\n")
        print(sotto_prodotti.value_counts())
        print("PANDAS: Query fatta in {} seconds".format(time.time() - start))
       
        # Altro modo di farlo:
        df.query('Product == "Mortgage"')['Sub-product'].value_counts()

        self.conection = MariaDBManagement()
        self.conection.connect_db("complaints")

        _cursor = self.cnx.cursor()
        try:
            start = time.time()
            _cursor.execute("""SELECT r.Sottoprodotto, count(*) FROM Reclami r 
                    where Prodotto = 'Mortgage' GROUP by r.Sottoprodotto""")
            rows = _cursor.fetchmany(size=200)
            print("MARIADB: Query fatta in {} seconds".format(time.time() - start))
        except Exception as e:
            print("Error executing statement select")
            print(e)

    def str_to_date(self, str_date):
        #2020-01-17
        new_date = []
        if isinstance(str_date, pd.Series):
            for idx, value in str_date.items():
                new_date.append(self.str_to_date(value))
            # new_date = pd.Series
        elif str_date is not None and len(str_date) > 0:
            date_parts = str_date.split('-')
            new_date = pd.Timestamp(year=int(date_parts[0]), month=int(date_parts[1]), day=int(date_parts[2]))
        return new_date

    def consent_to_boolean(self, str_consent):
        # Consent provided        550741
        # Consent not provided    413454
        # Other                    36723
        # Consent withdrawn         1966
        new_consent = []
        for idx, value in str_consent.items():
            if value == 'Consent provided':
                new_consent.append(True)
            elif value == 'Other':
                new_consent.append(np.nan)
            else:
                new_consent.append(False)

    def test_pulizia_dati(self):
        filepath = self.BASE_PATH + "/mockups/complaints.csv"
        df = pd.read_csv(filepath)
        # Prendiamo l'informazione dell'attuale dataframe
        print(df.info())
        print("\n")
        print(df[['Date received', 'Product', 'Sub-product']].head())
        print(df[['Issue', 'Sub-issue', 'Company', 'State']].head())
        print(df[['Consumer complaint narrative', 'Company public response']].head())
        print(df[['ZIP code', 'Tags', 'Consumer consent provided?', 'Submitted via', 'Date sent to company', 'Company response to consumer']].head())
        # Come questi dati sono nulli per le prime righe, filtriamo per quelli che non sia nulli e le visualiziamo
        print(df[df['Consumer disputed?'].notna()]['Consumer disputed?'].head())
        print(df[df['Tags'].notna()]['Tags'].head())
        """
        Date received --> pandas.Timestamp
        Product       --> pandas.StringDType()
        Sub-product   --> pandas.StringDType()
        Issue         --> pandas.StringDType()
        Sub-issue     --> pandas.StringDType()
        Consumer complaint narrative  --> pandas.StringDType()
        Company public response       --> pandas.StringDType()
        Company       --> pandas.StringDType()
        State         --> pandas.StringDType()
        ZIP code      --> pandas.StringDType()
        Tags          --> pandas.StringDType()
        Consumer consent provided?    --> pandas.BooleanDtype()
        Submitted via                 --> pandas.StringDType()
        Date sent to company          --> pandas.Timestamp
        Company response to consumer  --> pandas.StringDType
        Timely response?              --> pandas.BooleanDtype()
        Consumer disputed?            --> pandas.BooleanDtype()
        """
        date_recieved = df['Date received']
        new_date_recieved = date_recieved.map(self.str_to_date)

        # new_data = self.str_to_date(date_recieved)
        # new_date_recieved = pd.Series(name='Date received', data=new_data)
        print(new_date_recieved)
        df['Date received'] = new_date_recieved
        print(df['Date received'])

        product = pd.Series(data=df['Product'], dtype=pd.StringDtype())
        print(product)
        df['Product'] = product
        
        sproduct = pd.Series(data=df['Sub-product'], dtype=pd.StringDtype())
        print(sproduct)
        df['Sub-product'] = sproduct

        issue = pd.Series(data=df['Issue'], dtype=pd.StringDtype())
        print(issue)
        df['Issue'] = issue
        
        consent_provided = df['Consumer consent provided?']
        print(consent_provided.value_counts())

        new_data = self.consent_to_boolean(consent_provided)
        new_consent = pd.Series(name='Consent provided', data=new_data)
        df['Consumer consent provided?'] = new_consent

        print(df.info())

    def color_negative_red(val):
        """
        Takes a scalar and returns a string with
        the css property `'color: red'` for negative
        strings, black otherwise.
        """
        color = 'red' if val <= 0 else 'black'
        return 'color: %s' % color
        
    def test_style(self):
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html
        filepath = self.BASE_PATH + "/mockups/time_series_covid19_confirmed_global.csv"
        codvid_df = pd.read_csv(filepath)

        media = codvid_df['1/22/20'].mean()
        moda = codvid_df['Country/Region'].mode()
        # mode ritorna un Series e noi volgiamo un valore
        moda_value = moda.array[0]

        """ Nota:

        if x<=media:
            return  '#D2D43E'
        else:
            return 'orange'

        '#D2D43E' if x<=media else 'orange'
        '#D2D43E' ? x<=media : 'orange'
        """
        new_styler = codvid_df.style.applymap(lambda x: 'background-color: %s' % ('#D2D43E' if x<=media else 'orange'), subset=['1/22/20', '1/23/20'])
        new_styler2 = new_styler.applymap(lambda x: 'color: %s' % ('red' if x==moda_value else 'white'), subset=['Country/Region'])
        html_code = new_styler2.render()
        with open('index.html', 'w') as f:
            f.write(html_code)

    def test_pivote(self):
        df = pd.DataFrame({
                   "A": ["foo", "foo", "foo", "foo", "foo",
                         "bar", "bar", "bar", "bar"],
                   "B": ["one", "one", "one", "two", "two",
                         "one", "one", "two", "two"],
                   "C": ["small", "large", "large", "small",
                         "small", "large", "small", "small",
                         "large"],
                   "D": [1, 2, 2, 3, 3, 4, 5, 6, 7],
                   "E": [2, 4, 5, 5, 6, 6, 8, 9, 9]}
        )
        print(df)

        table = pd.pivot_table(df, values='D', index=['A', 'B'],
                    columns=['C'], aggfunc=np.sum, fill_value=0)
        print("Pivote:\n", table)

        table = pd.pivot_table(df, values='D', index=['A', 'B'],
                    columns=['C'], aggfunc=np.sum, fill_value=0)
        print("Agregata:\n", table)

    def test_multiindex(self):
        df = pd.DataFrame([[1,2],[3,4]])
        print("Senza multiindex:\n", df)
        df.index = pd.MultiIndex.from_tuples([('a', 'b'), ('a', 'c')])
        print("Con multiindex:\n", df)
        df.columns = ["x","y"]
        html_code = df.style.apply('border-style: black').render()
        with open('index.html', 'w') as f:
            f.write(html_code)

    def test_groupby(self):
        filepath = self.BASE_PATH + "/mockups/time_series_covid19_confirmed_global.csv"
        df = pd.read_csv(filepath)
        print("Soltanto colonna Country/Region count:\n", df['Country/Region'].value_counts())
        print("Con group by:\n", df.groupby('Country/Region')['Country/Region'].count().sort_values(ascending=False))
