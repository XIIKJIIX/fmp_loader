from datetime import date
from decimal import Decimal
from typing import Dict, Optional


from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase, config
from marshmallow import fields


def maybe_parse_date(date_str: str) -> Optional[date]:
    try:
        parsed_date = date.fromisoformat(date_str)
        return parsed_date
    except ValueError:
        return None


def parse_decimal_from_float(val: float):
    return Decimal(str(val))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class HistoricalDividend:
    symbol: str
    label: str
    adj_dividend: Decimal = field(
        metadata=config(
            decoder=parse_decimal_from_float, mm_field=fields.Decimal(28, 9)
        )
    )
    dividend: Decimal = field(
        metadata=config(
            decoder=parse_decimal_from_float, mm_field=fields.Decimal(28, 9)
        )
    )
    record_date: Optional[date] = field(
        metadata=config(decoder=maybe_parse_date, mm_field=fields.Date(format="iso"))
    )
    payment_date: Optional[date] = field(
        metadata=config(decoder=maybe_parse_date, mm_field=fields.Date(format="iso"))
    )
    declaration_date: Optional[date] = field(
        metadata=config(decoder=maybe_parse_date, mm_field=fields.Date(format="iso"))
    )
    # Renamed from `date` to `identifier_date` due to dataclass_json
    # recursion error when parsing this field
    identifier_date: date = field(
        metadata=config(
            field_name="date",
            decoder=maybe_parse_date,
            mm_field=fields.Date(format="iso"),
        )
    )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DelistedCompany:
    symbol: str
    company_name: str
    exchange: str
    ipo_date: date = field(
        metadata=config(decoder=maybe_parse_date, mm_field=fields.Date(format="iso"))
    )
    delisted_date: date = field(
        metadata=config(decoder=maybe_parse_date, mm_field=fields.Date(format="iso"))
    )
