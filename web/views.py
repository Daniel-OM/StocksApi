
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

# checKey = lambda k, dic: dic[k] if k in dic else None
def checKey(k, dic):
    return dic[k] if k in dic else None

# entityToDict = lambda entity, hidden_fields: {k: v for k, v in entity.__dict__.items() if k not in hidden_fields}
def entityToDict(entity, hidden_fields:list=[]) -> dict:
    
    return {k: v for k, v in entity.__dict__.items() if k not in hidden_fields}


def getYahooData(text:str) -> dict:

    ys = YahooFinance(verbose=True)
    ticker: str = ys.searchText(text)['quotes'][0]['symbol']
    result: dict = ys.getKPI(ticker=ticker)
    info: dict = ys.getCompanyInfo(ticker=ticker, info=['assetProfile'])['quoteSummary']['result'][0]['assetProfile']
    quote: dict = ys.getQuote(ticker=ticker)['quoteResponse']['result'][0]
    income_sheet: dict = ys.getFinancials(ticker=ticker)['quoteSummary']['result'][0]
    balance_sheet: dict = ys.getFundamentalTimeseries(ticker=ticker, 
        fundamentals=['annualTotalAssets', 'annualTotalLiabilitiesNetMinorityInterest'])['timeseries']['result']
    
    result['Ticker'] = ticker
    result['Company'] = quote['longName']
    result['Exchange'] = quote['fullExchangeName']
    result['Price'] = {'Value': quote['regularMarketPrice']['raw'], 
                    'Time': quote['regularMarketTime']['fmt']}
    result['Sector'] = info['sector']
    result['Sub-Sector'] = info['industry']
    result['Country'] = info['country']
    result['Employees'] = info['fullTimeEmployees']
    result['Description'] = info['longBusinessSummary']
    result['Revenue'] = {'TTM': sum([i['totalRevenue']['raw'] for i in income_sheet['incomeStatementHistoryQuarterly']['incomeStatementHistory']]), 
            'Last':income_sheet['incomeStatementHistory']['incomeStatementHistory'][0]['totalRevenue']['fmt']}
    result['Net-Earnings'] = {'TTM':sum([i['netIncome']['raw'] for i in income_sheet['incomeStatementHistoryQuarterly']['incomeStatementHistory']]), 
            'Last':income_sheet['incomeStatementHistory']['incomeStatementHistory'][0]['netIncome']['fmt']}
    result['Assets'] = balance_sheet[0]['annualTotalAssets'][-1]['reportedValue']['fmt']
    result['Liabilities'] = balance_sheet[1]['annualTotalLiabilitiesNetMinorityInterest'][-1]['reportedValue']['fmt']
    
    # bz = Benzinga(symbol=ticker)
    # bz.info()
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
        
        if data['company'] != '':
            ticker, data = getYahooData(data['company'])
        elif data['symbol'] != '':
            ticker, data = getYahooData(data['symbol'])
        else:
            message = 'ERROR: There was an error while runing the search! There are no company or symbol.'
        
        bzdata = getBenzingaData(ticker)
        
        return render_template('ticker.html', data=data, message=message)
    else:
        
        return render_template('ticker.html')

@views.route("/about")
def about() -> str:
    return render_template('about.html')
