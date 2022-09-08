
import argparse
from asyncio.log import logger
import os
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)

from dotenv import load_dotenv

from fmp_loader.repository import Datasource, DelistedCompanyAbstractRepository, DelistedCompanySqlRepository, FmpLocalFileDatasource, FmpRestApiDatasource, HistoricalDividendAbstractRepository, HistoricalDividendSqlRepository

def load_historical_dividend(repo: HistoricalDividendAbstractRepository, ds: Datasource, symbol: str):
  historical_dividends = ds.fetch_historical_dividends(symbol)
  logging.info(f"Found {len(historical_dividends)} historical dividends for {symbol}")
  repo.upsert_many(historical_dividends)
  logging.info(f"Completed load historical dividends for {symbol}")
  

def load_delisted_companies(repo: DelistedCompanyAbstractRepository, ds: Datasource, page: int = 0):
  delisted_companies = ds.fetch_delisted_companies(page)
  logging.info(f"Found {len(delisted_companies)} delisted companies")
  repo.upsert_many(delisted_companies)
  logging.info(f"Completed load delisted companies")


if __name__ == '__main__':

  load_dotenv()

  parser = argparse.ArgumentParser(description='Load data from financialmodelingprep.com into a database', prog='fmp_loader')
  sg = parser.add_mutually_exclusive_group(required=True)
  sg.add_argument('--local', metavar='FILE_PATH', help='Load data from local file')
  sg.add_argument('--api', help='Load data from FMP API, an FMP_API_KEY is required in .env file', action='store_true')
  sp = parser.add_subparsers(dest="subparser_name")
  hd_sp = sp.add_parser('historical_dividend', help='Load historical dividend data')
  hd_sp.add_argument('--symbol', metavar='SYMBOL', type=str, nargs='?',
                      help='load historical dividend data for the given symbol', required=True)
  dc_sp = sp.add_parser('delisted_company', help='Load delisted companies data')
  dc_sp.add_argument('--page', metavar='PAGE', type=int, nargs='?',
                      help='load delisted companies data for the given page, if not specified, default is 0 (doesn\'t work with local file)', default=0)  

  args = parser.parse_args()


  db = create_engine(os.getenv('DATABASE_URL'))

  if args.local:
    logging.info(f"Loading data from local file: {args.local}")
    ds = FmpLocalFileDatasource(args.local)

  if args.api:
    ds = FmpRestApiDatasource(os.getenv('FMP_API_KEY'))
  
  if args.subparser_name == 'historical_dividend':
    logging.info(f"Loading historical dividend data for symbol: {args.symbol}")
    repo = HistoricalDividendSqlRepository(db)
    load_historical_dividend(repo, ds, args.symbol)

  if args.subparser_name == 'delisted_company':
    logging.info(f"Loading delisted companies data for page: {args.page}")
    repo = DelistedCompanySqlRepository(db)
    load_delisted_companies(repo, ds, args.page)

