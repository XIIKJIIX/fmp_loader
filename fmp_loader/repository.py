import abc
from typing import List
import json
import os
from sqlalchemy.engine.base import Engine
from sqlalchemy import text

import requests

from .model import HistoricalDividend, DelistedCompany

class HistoricalDividendAbstractRepository(abc.ABC):
    @abc.abstractmethod 
    def upsert(self, hd: HistoricalDividend):
        raise NotImplementedError

    @abc.abstractmethod 
    def upsert_many(self, hds: List[HistoricalDividend]):
        raise NotImplementedError

class HistoricalDividendSqlRepository(HistoricalDividendAbstractRepository):
  upsert_stmt = text("""
INSERT INTO historical_dividend (symbol, date, label, adj_dividend, dividend, record_date, payment_date,
                                 declaration_date)
VALUES (:symbol, :identifier_date, :label, :adj_dividend, :dividend, :record_date, :payment_date, :declaration_date)
ON CONFLICT (symbol, date) DO UPDATE
    SET label            = :label,
        adj_dividend     = :adj_dividend,
        dividend         = :dividend,
        record_date      = :record_date,
        payment_date     = :payment_date,
        declaration_date = :declaration_date;
""")

  def __init__(self, db: Engine) -> None:
      self.db = db

  def upsert(self, hd: HistoricalDividend):
    with self.db.begin() as conn:
      conn.execute(self.upsert_stmt, **hd.__dict__)

  def upsert_many(self, hds: List[HistoricalDividend]):
     with self.db.begin() as conn:
        for hd in hds:
          conn.execute(self.upsert_stmt, **hd.__dict__)


class DelistedCompanyAbstractRepository(abc.ABC):
  @abc.abstractmethod 
  def upsert(self, dc: DelistedCompany):
      raise NotImplementedError

  @abc.abstractmethod 
  def upsert_many(self, dcs: List[DelistedCompany]):
      raise NotImplementedError

class DelistedCompanySqlRepository(DelistedCompanyAbstractRepository):
  upsert_stmt = text("""
INSERT INTO delisted_company (symbol, company_name, exchange, ipo_date, delisted_date)
VALUES (:symbol, :company_name, :exchange, :ipo_date, :delisted_date)
ON CONFLICT (symbol, exchange, ipo_date) DO UPDATE
    SET company_name  = :company_name,
        delisted_date = :delisted_date;
""")

  def __init__(self, db: Engine) -> None:
    self.db = db

  def upsert(self, dc: DelistedCompany):
    with self.db.begin() as conn:
      conn.execute(self.upsert_stmt, **dc.__dict__)

  def upsert_many(self, dcs: List[DelistedCompany]):
     with self.db.begin() as conn:
        for dc in dcs:
          conn.execute(self.upsert_stmt, **dc.__dict__)


class Datasource(abc.ABC):
  @abc.abstractmethod 
  def fetch_historical_dividends(self, symbol:str):
    raise NotImplementedError

  @abc.abstractmethod 
  def fetch_delisted_companies(self, page: int = 0):
    raise NotImplementedError

class FmpRestApiDatasource(Datasource):
  def __init__(self, api_key: str) -> None:
     self.api_key = api_key

  def fetch_historical_dividends(self, symbol: str) -> List[HistoricalDividend]:
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{symbol}?apikey={self.api_key}"
    data = requests.get(url).json()
    if "historical" not in data:
      return []
    return [HistoricalDividend.from_dict({**d, "symbol": symbol}) for d in data["historical"]]

  def fetch_delisted_companies(self, page: int = 0) -> List[DelistedCompany]:
    url = f"https://financialmodelingprep.com/api/v3/delisted-companies?page={page}&apikey={self.api_key}"
    data = requests.get(url).json()
    return [DelistedCompany.from_dict(d) for d in data]

class FmpLocalFileDatasource(Datasource):
  def __init__(self, file_path: str) -> None:
    self.file_path = file_path

  def fetch_historical_dividends(self, symbol: str) -> List[HistoricalDividend]:
    with open(self.file_path, "r") as f:
      data = json.load(f)
      return [HistoricalDividend.from_dict({**d, "symbol": symbol}) for d in data["historical"]]

  def fetch_delisted_companies(self, page: int = 0) -> List[DelistedCompany]:
    with open(self.file_path, "r") as f:
      data = json.load(f)
      return [DelistedCompany.from_dict(d) for d in data]
