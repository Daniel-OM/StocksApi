
import requests
from bs4 import BeautifulSoup

def getTextSymbol(text:str): 
    
    url = 'https://query2.finance.yahoo.com/v1/finance/search'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
    params = {
        'q':text,
        'lang':'en-US',
        'region':'US',
        'quotesCount':'6',
        'newsCount':'2',
        'listsCount':'2',
        'enableFuzzyQuery':'false',
        'quotesQueryId':'tss_match_phrase_query',
        'multiQuoteQueryId':'multi_quote_single_token_query',
        'newsQueryId':'news_cie_vespa',
        'enableCb':'true',
        'enableNavLinks':'true',
        'enableEnhancedTrivialQuery':'true',
        'enableResearchReports':'true',
        'enableCulturalAssets':'true',
        'enableLogoUrl':'true',
        'researchReportsCount':'2'
    }
    r = requests.get(url, params=params, headers=headers)
    
    return r.json()['quotes'][0]['symbol']

def getMain(ticker:str) -> dict:

    ticker = getTextSymbol(ticker)

    url = f'https://finance.yahoo.com/quote/{ticker}?.tsrc=fin-srch'
    r = requests.get(url)
    html = BeautifulSoup(r.content, 'html.parser')

    head = html.find('div', attrs={'id': 'quote-header-info'})
    info = [e.get_text() for i, e in enumerate(html.find('p', attrs={'class':'D(ib) Va(t)'}).find_all('span')) if i%2 != 0]
    result = {
        'Ticker': head.find('h1').get_text().split(' (')[-1].replace(')', ''), #
        'Company': head.find('h1').get_text().split(' (')[0], #
        'Logotype': '',
        'Exchange': head.find('div', attrs={'class': 'C($tertiaryColor)'}).get_text().split(' -')[0],
        'Contry': [s for s in html.find('p', attrs={'class':'D(ib) W(47.727%) Pend(40px)'}).strings][-3], #
        'Sector': info[0],
        'Sub-Sector': info[1],
        'Employees': info[2],
        'Price': {'Value': html.find('fin-streamer', attrs={'data-test':'qsp-price'})['value'], 
                  'Time': html.find('div', attrs={'id':'quote-market-notice'}).get_text().split('  ')[-1]},
        'BPA': html.find('td', attrs={'data-test': 'EPS_RATIO-value'}).get_text(), # EPS
        'PER': html.find('td', attrs={'data-test': 'PE_RATIO-value'}).get_text(),
        'BETA': html.find('td', attrs={'data-test': 'BETA_5Y-value'}).get_text(),
        'Revenue': {'TTM': 385706000, 'Last':383285000},
        'Net-Earnings': {'TTM':100913000, 'Last':96995000},
        'Assets': 352583000,
        'Liabilities': 290437000,
        'Description': html.find('p', attrs={'class':'businessSummary'}).get_text()
    }

    return result

def getStatistics():
    url = 'https://finance.yahoo.com/quote/AAPL/key-statistics'
    url = 'https://finance.yahoo.com/quote/AAPL/balance-sheet'
    url = 'https://finance.yahoo.com/quote/AAPL/financials'
    r = requests.get(url)
    html = BeautifulSoup(r.content, 'html.parser')

