
import datetime as dt
import sqlite3
import json
import sys

import numpy as np
import pandas as pd

sys.path.append('..')

from flask import Blueprint, flash, redirect, render_template, request, url_for

from .static.python.benzinga import Benzinga
from .static.python.yahoo import YahooFinance

# checKey = lambda k, dic: (dic[k] if k in dic else None) if dic != None else None
def checKey(keys:(int | str | list[str]), dic:dict):

    if isinstance(keys, list):
        value: dict = dic
        for key in keys:
            if key in value:
                value = value[key]
            else:
                value = None
                break
        return value
    else:
        return (dic[keys] if keys in dic else None) if dic != None else None

# entityToDict = lambda entity, hidden_fields: {k: v for k, v in entity.__dict__.items() if k not in hidden_fields}
def entityToDict(entity, hidden_fields:list=[]) -> dict:
    return {k: v for k, v in entity.__dict__.items() if k not in hidden_fields}


def getYahooData(text:str) -> dict:

    ys = YahooFinance(verbose=True)
    ticker: str = ys.searchText(text)['quotes'][0]['symbol']

    info: dict = ys.getCompanyInfo(ticker=ticker, info=['assetProfile'])['quoteSummary']['result'][0]['assetProfile']
    quote: dict = ys.getQuote(ticker=ticker)['quoteResponse']['result'][0]
    finance: dict = ys.getFinancials(ticker=ticker, financials=ys.getDataAvailable())['quoteSummary']['result'][0]
    balance_sheet: list = ys.getFundamentalTimeseries(ticker=ticker,
        fundamentals=ys.getAvailableFundamentals())['timeseries']['result']
    balance_sheet: list = {k: [i for i in v if i != None] for d in balance_sheet if len(d.keys()) > 1 \
                           for k, v in d.items() if k not in ['meta', 'timestamp']}
    insights: dict = ys.getInsights(ticker=ticker)['finance']['result'][0]
    price_raw: dict = ys.getPrice(ticker=ticker, interval='1m')['chart']['result'][0]
    trading_periods = {
        'pre': {'start': dt.datetime.fromtimestamp(price_raw['meta']['currentTradingPeriod']['pre']['start']).time(),
                'end':dt.datetime.fromtimestamp(price_raw['meta']['currentTradingPeriod']['pre']['end']).time()},
        'regular': {'start': dt.datetime.fromtimestamp(price_raw['meta']['currentTradingPeriod']['regular']['start']).time(),
                'end':dt.datetime.fromtimestamp(price_raw['meta']['currentTradingPeriod']['regular']['end']).time()},
        'post': {'start': dt.datetime.fromtimestamp(price_raw['meta']['currentTradingPeriod']['post']['start']).time(),
                'end':dt.datetime.fromtimestamp(price_raw['meta']['currentTradingPeriod']['post']['end']).time()}
    }
    def checkDateSession(date:dt.datetime, trading_periods:dict):
        for session, v in trading_periods.items():
            if v['start'] <= date.time() and date.time() < v['end']:
                return session
        return None
    dates: list = [dt.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M') for date in price_raw['timestamp']]
    prices: pd.DataFrame = pd.DataFrame([{k: v[i] for k, v in price_raw['indicators']['quote'][0].items()} \
                               for i in range(len(dates))])
    data: dict = {
        'date': dates,
        'price': prices.loc[:,['open', 'close', 'low', 'high']].values.tolist(),
        'volume': prices.loc[:,'volume'].tolist(),
    }
    # data: dict = [{**{'date': d},
    #                **{k: v[i] for k, v in price_raw['indicators']['quote'][0].items()},
    #                **{'session':checkDateSession(d, trading_periods)}} \
    #               for i, d in enumerate(dates)]

    # bz = Benzinga(symbol=ticker)
    # bz.info()

    result: dict = {
        'ticker': ticker,
        'company': checKey('longName', quote),
        'exchange': checKey('fullExchangeName', quote),
        'type': checKey('quoteType', quote),
        'time_zone': checKey('exchangeTimezoneName', quote),
        'sector': checKey('sector', info),
        'sub_sector': checKey('industry', info),
        'employees': checKey('fullTimeEmployees', info),
        'description': checKey('longBusinessSummary', info),
        'address': checKey('address1', info),
        'city': checKey('city', info),
        'zip': checKey('zip', info),
        'country': checKey('country', info),
        'phone': checKey('phone', info),
        'website': checKey('website', info),
        'logotype': '',
        'ipo': dt.datetime.fromtimestamp(checKey('firstTradeDate', price_raw)).strftime('%Y-%m-%d') 
                if checKey('firstTradeDate', price_raw) else None,
        'price': {'raw': checKey(['price', 'regularMarketPrice', 'raw'], finance), 
                  'fmt': checKey(['price', 'regularMarketPrice', 'fmt'], finance)},
        'volume': {'raw': checKey(['price', 'regularMarketVolume', 'raw'], finance), 
                  'fmt': checKey(['price', 'regularMarketVolume', 'fmt'], finance)},
        'eps': {'raw': checKey(['financialData', 'revenuePerShare', 'raw'], finance), 
                  'fmt': checKey(['financialData', 'revenuePerShare', 'fmt'], finance)},
        'per': {'raw': checKey(['summaryDetail', 'forwardPE', 'raw'], finance), 
                  'fmt': checKey(['summaryDetail', 'forwardPE', 'fmt'], finance)},
        'beta': {'raw': checKey(['summaryDetail', 'beta', 'raw'], finance), 
                  'fmt': checKey(['summaryDetail', 'beta', 'fmt'], finance)},
        'dividend': {'raw': checKey(['summaryDetail', 'dividendYield', 'raw'], finance), 
                  'fmt': checKey(['summaryDetail', 'dividendYield', 'fmt'], finance)},
        'avg_volume': {'raw': checKey(['summaryDetail', 'averageVolume', 'raw'], finance), 
                  'fmt': checKey(['summaryDetail', 'averageVolume', 'fmt'], finance)},
        'earnings_date': checKey(['earnings','earningsChart','earningsDate'], finance)[0]['fmt'],
        'assets': checKey('annualTotalAssets', balance_sheet)[-1]['reportedValue']['fmt'],
        'liabilities': checKey('annualTotalLiabilitiesNetMinorityInterest', balance_sheet)[-1]['reportedValue']['fmt'],
        'bullish_stories': checKey(['upsell', 'msBullishSummary'], insights),
        'bearish_stories': checKey(['upsell', 'msBearishSummary'], insights),
        'candles': data,
        'balance_sheet': {''.join([('_'+s.lower() if s.isupper() else s) for s in k]): v for k,v in balance_sheet.items()},
    }

    if checKey('secReports', insights):
        reports: pd.DataFrame = pd.DataFrame(checKey('secReports', insights))
        reports.columns = [''.join([('_'+s.lower() if s.isupper() else s) for s in c]) for c in reports.columns]
        reports['filing_date'] = pd.to_datetime(reports['filing_date']*1e6).dt.strftime('%Y-%m-%d')
        reports: pd.DataFrame = reports.loc[:,['filing_date', 'form_type', 'type', 'description']]
        result['sec_fillings'] = {'columns': reports.columns.tolist(), 'data': reports.values.tolist()}
    
    if checKey(['earnings', 'earningsChart'], finance):
        result['earnings'] = [{'date':checKey('date', e), 'actual':checKey(['actual', 'raw'], e), 'estimate':checKey(['estimate', 'raw'], e)} \
                     for e in  checKey(['earnings', 'earningsChart', 'quarterly'], finance)] + \
                    [{'date': f"{checKey(['earnings','earningsChart','currentQuarterEstimateDate'], finance)}{checKey(['earnings','earningsChart','currentQuarterEstimateYear'], finance)}",
                      'actual': None, 'estimate': checKey(['earnings','earningsChart','currentQuarterEstimate','raw'], finance)}]
    else:
        result['earnings'] = None
        
    if checKey('companyOfficers', info):
        result['officers'] = {'columns':['name', 'age', 'title', 'year_born'], 
                              'data':[[(o[k] if k in o else None) for k in ['name', 'age', 'title', 'yearBorn']] for o in checKey('companyOfficers', info)]}
    else:
        result['officers'] = None

    if checKey(['earnings', 'financialsChart'], finance):
        result['revenue'] = [{'date':checKey('date', e), 'revenue':checKey(['revenue', 'raw'], e), 'earnings':checKey(['earnings', 'raw'], e)} \
                     for e in  checKey(['earnings', 'financialsChart', 'yearly'], finance)]
        result['last_revenue'] = checKey(['earnings', 'financialsChart', 'yearly'], finance)[-1]['revenue']['fmt'] \
                                if checKey(['earnings', 'financialsChart', 'yearly'], finance) else None
        result['last_net_earnings'] = checKey(['earnings', 'financialsChart', 'yearly'], finance)[-1]['earnings']['fmt'] \
                                if checKey(['earnings', 'financialsChart', 'yearly'], finance) else None
    else:
        result['revenue'] = None
        result['last_revenue'] = None
        result['last_net_earnings'] = None

    return ticker, result

def getBenzingaData(ticker:str) -> dict:

    bz = Benzinga(ticker)
    result: dict = {}
    for k, v in bz.info().items():
        if k in ['dateUpdated', 'image', 'primarySymbol', 'primaryExchange', 'cik', 'isin', 'cusip',
                 'standardName', 'yearofEstablishment', 'shortName', 'address1', 'city', 'country', 
                 'homepage', 'phone', 'postalCode', 'province', 'totalEmployees', 'legalName', 'longDescription',
                 'currencyId', 'ipoDate', 'sicName', 'naicsName', 'msSuperSectorName', 'msSectorName', 
                 'msGroupName', 'msIndustryName']:
            result[k] = v
    # classification = bz.classification()
    # result['marketCap'] = bz.marketCap()
    for k, v in bz.shareData().items():
        if k in ['bzExchange', 'type', 'lastTradePrice', 'lastTradeTime', 'volume', 'fiftyDayAveragePrice', 
                 'hundredDayAveragePrice', 'averageVolume', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 
                 'marketCap', 'sharesOutstanding', 'sharesFloat']:
            result[k] = v
    result['schedule'] = bz.schedule()
    result['valuations'] = bz.valuations()
    result['balanceSheet'] = bz.balanceSheet()
    result['cashFlow'] = bz.cashFlow()
    result['incomeStatement'] = bz.incomeStatement()
    result['operationRatios'] = bz.operationRatios()
    # listFilling = bz.listFilling()
    result['earnings'] = bz.earnings()
    result['dividends'] = bz.dividends()
    result['splits'] = bz.splits(df=False)
    result['ownership'] = bz.ownership()
    result['shortInterest'] = bz.shortInterest(df=False)
    result['mergersAcquisitions'] = bz.mergersAcquisitions(df=False)
    result['news'] = bz.news(df=False)
    # data = bz.keyData()
    relatedStocks = bz.relatedStocks()
    result['relatedStocks'] = (relatedStocks['companyStandardName'] + ' (' + relatedStocks['symbol'] + ':' + relatedStocks['bzExchange'] +')').to_list()
    # percentileStats = bz.percentileStats()
    result['earningsHistoric'] = bz.earningsHistoric()

    return result

views = Blueprint(name='views', import_name=__name__)

@views.route("/")
def home() -> str:
    return render_template('home.html')

@views.route("/ticker", methods=["GET", "POST"])
def ticker():
    
    if request.method == 'POST':
        
        message = ''

        data = {k: v[0] if len(v) == 1 else v
            for k, v in request.form.to_dict(flat=False).items() if v or v > 0 or len(v) > 0}
        print(data)
        
        if data['company'] != '':
            ticker, data = getYahooData(data['company'])
        elif data['symbol'] != '':
            ticker, data = getYahooData(data['symbol'])
        else:
            message = 'ERROR: There was an error while runing the search! There are no company or symbol.'
        
        # bzdata = getBenzingaData(ticker)
        print(data)
        
        return render_template('ticker.html', data=data, message=message)
    else:
        
        return render_template('ticker.html')

@views.route("/about")
def about() -> str:
    return render_template('about.html')
