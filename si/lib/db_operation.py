import psycopg2 as db
import pandas as pd
import numpy as np

# Columns Name #
COMPANY_COLUMN_LIST = ['symbol', 'name', 'ipo_year', 'sector', 'industry']

QUOTE_COLUMN_LIST = ['quote_date', 'open', 'close', 'high', 'low', 'volume']

# Select SQL #
SELECT_ALL_COMPANIES_SQL = 'SELECT com.symbol, com.name, com.ipo_year, com.sector, com.industry \
    FROM company com'

SELECT_COMPANY_WITH_STATISTICS_SQL = 'SELECT com.id, com.symbol, com.name, com.sector, com.last_quote_dt, st.insider_own_perc, st.inst_own_perc, st.shs_outstand, st.shs_float \
    FROM company com JOIN company_statistics st ON com.id = st.company_id'

SELECT_QUOTES_BY_SYMBOL_SQL = 'SELECT quo.quote_date, quo.open, quo.close, quo.high, quo.low, quo.volume \
    FROM stock_quote quo JOIN company com ON com.id = quo.company_id \
    WHERE com.symbol LIKE \'%s\' \
    ORDER BY quo.quote_date ASC'


class DBService:

    def __init__(self, database='ps', user='postgres', password='123456', host='localhost', port='5432'):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = db.connect(database=self.database, user=self.user, password=self.password, host=self.host,
                               port=self.port)
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.conn.close()

    def get_companies(self):
        """

        Returns:
            DataFrame of companies
        """
        self.cursor.execute(SELECT_ALL_COMPANIES_SQL)
        # return np.array(self.cursor.fetchall())
        return pd.DataFrame(data=self.cursor.fetchall(), columns=COMPANY_COLUMN_LIST)

    def get_quotes_by_symbol(self, symbol):
        """
        Get the quotes DataFrame specified by symbol.
        Args:
            symbol: str
                The stock symbol.

        Returns:

        """
        self.cursor.execute(SELECT_QUOTES_BY_SYMBOL_SQL % symbol)
        return pd.DataFrame(data=self.cursor.fetchall(), columns=QUOTE_COLUMN_LIST)

    def get_all_company_quotes(self, company_filter_func=lambda quotes: np.all(quotes.volume > 100)):
        """

        Args:
            company_filter_func: function, default filter volume less than 100.
                A function that operates on all quotes of a company. When it returns true, keep the company's quotes,
                otherwise drop the company's quotes.

        Returns:
            A dict with key that's stock symbol and value that's quotes
        """
        companies = self.get_companies()
        all_quotes = {}
        for symbol in companies.symbol.values:
            quotes = self.get_quotes_by_symbol(symbol)
            # filter quotes
            if company_filter_func is None or company_filter_func(quotes):
                all_quotes[symbol] = quotes

        return all_quotes

    def get_all_company_quotes_iterator(self, company_filter_func=lambda quotes: np.all(quotes.volume > 100)):
        """

        Args:
            company_filter_func: function, default filter volume less than 100.
                A function that operates on all quotes of a company. When it returns true, keep the company's quotes,
                otherwise drop the company's quotes.

        Returns:
            A tuple like (company, quotes)
        """
        companies = self.get_companies()
        for _, company in companies.iterrows():
            symbol = company['symbol']
            quotes = self.get_quotes_by_symbol(symbol)
            # filter quotes
            if company_filter_func is None or company_filter_func(quotes):
                yield company, quotes

    def execute_sql(self, sql):
        self.cursor.execute(sql)
        return np.array(self.cursor.fetchall())
