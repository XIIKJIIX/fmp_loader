from datetime import date
from decimal import Decimal
from fmp_loader import __version__
from fmp_loader.model import DelistedCompany, HistoricalDividend


def test_version():
    assert __version__ == "0.1.0"


def test_parse_historical_dividend():
    hd = HistoricalDividend.from_dict(
        {
            "symbol": "AAPL",
            "date": "2022-08-05",
            "label": "August 05, 22",
            "adjDividend": 0.23,
            "dividend": 0.23,
            "recordDate": "",
            "paymentDate": "",
            "declarationDate": "2022-07-28",
        }
    )

    assert hd.symbol == "AAPL"
    assert hd.identifier_date == date(2022, 8, 5)
    assert hd.label == "August 05, 22"
    assert hd.adj_dividend == Decimal("0.23")
    assert hd.dividend == Decimal("0.23")
    assert hd.record_date == None
    assert hd.payment_date == None
    assert hd.declaration_date == date(2022, 7, 28)


def test_parse_delisted_company():
    dc = DelistedCompany.from_dict(
        {
            "symbol": "AAPL",
            "companyName": "Apple Inc",
            "exchange": "NASDAQ",
            "ipoDate": "1980-12-12",
            "delistedDate": "2021-04-20",
        }
    )

    assert dc.symbol == "AAPL"
    assert dc.company_name == "Apple Inc"
    assert dc.exchange == "NASDAQ"
    assert dc.ipo_date == date(1980, 12, 12)
    assert dc.delisted_date == date(2021, 4, 20)
