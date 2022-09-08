
import argparse

from sqlalchemy import create_engine

from fmp_loader.repository import Datasource, DelistedCompanyAbstractRepository, DelistedCompanySqlRepository, HistoricalDividendAbstractRepository, HistoricalDividendSqlRepository

def load_historical_dividend(repo: HistoricalDividendAbstractRepository, ds: Datasource, symbol: str):
  historical_dividends = ds.fetch_historical_dividends(symbol)
  repo.upsert_many(historical_dividends)
  

def load_delisted_companies(repo: DelistedCompanyAbstractRepository, ds: Datasource, page: int = 0):
  delisted_companies = ds.fetch_delisted_companies(page)
  repo.upsert_many(delisted_companies)


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Load data from financialmodelingprep.com into a database')
  parser.add_argument('--historical-dividend', metavar='SYMBOL', type=str, nargs='?',
                      help='load historical dividend data for the given symbol')
  parser.add_argument('--delisted-companies', metavar='PAGE', type=int, nargs='?',
                      help='load delisted companies data for the given page')
  args = parser.parse_args()

  db = create_engine('')
  ds = FmpDatasource()

  if args.historical_dividend:
    load_historical_dividend(HistoricalDividendSqlRepository(db), ds, args.historical_dividend)
  elif args.delisted_companies:
    load_delisted_companies(DelistedCompanySqlRepository(db), ds, args.delisted_companies)
  else:
    parser.print_help()

