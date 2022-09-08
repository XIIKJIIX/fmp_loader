# Financial Modeling Prep Loader

Download data from [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs)

Currently support
- [Historical Dividend](https://site.financialmodelingprep.com/developer/docs#Historical-Dividends)
- [Delisted Companies](https://site.financialmodelingprep.com/developer/docs#Delisted-Companies)

## Prerequisite
Make sure that all of following tools are installed.
- Docker
- [Golang Migrate](https://github.com/golang-migrate/migrate) (`brew install golang-migrate`)
- Python 3.10
- [Poetry](https://python-poetry.org/docs/) (`brew install poetry`)

And then start a local Postgresql with
```bash
docker run -d --name pgdev  -p 5432:5432 -e POSTGRES_PASSWORD=secret postgres:14
```
Above command should start a local Postgresql container with `secret` as a password.

Run the following command to setup dependencies and activate the venv shell.
```bash
poetry install
poetry shell
```

Copy `.env.example` to `.env` and and fill in your FMP api key and database url.

And then run the following command to migrate a database
```bash
migrate -source file://migration -database 'postgres://postgres:secret@localhost:5432/postgres?sslmode=disable' up
```

## Up and Running

### Getting help
```bash
> python -m fmp_loader -h
usage: fmp_loader [-h] (--local FILE_PATH | --api) {historical_dividend,delisted_company} ...

Load data from financialmodelingprep.com into a database

positional arguments:
  {historical_dividend,delisted_company}
    historical_dividend
                        Load historical dividend data
    delisted_company    Load delisted companies data

options:
  -h, --help            show this help message and exit
  --local FILE_PATH     Load data from local file
  --api                 Load data from FMP API, an FMP_API_KEY is required in .env file
```

### Load from a local file
Historical Dividend
```bash
python -m fmp_loader --local sample_data/aapl_dividend.json historical_dividend --symbol AAPL
```

Delisted Companies
```bash
python -m fmp_loader --local sample_data/delisted_0.json delisted_company
```

### Load from an API
Historical Dividend
```bash
python -m fmp_loader --api   historical_dividend --symbol AAPL
```

Delisted Companies
```bash
python -m fmp_loader --api delisted_company --page 9
```


## Testing
```bash
pytest
```

## Linting
```bash
black .
```