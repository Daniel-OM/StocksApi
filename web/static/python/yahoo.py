
import enum

import requests
from bs4 import BeautifulSoup

from .data import DataProvider

class YahooFinance(DataProvider):

    class Method(enum.Enum):
        GET: str = 'GET'
        POST: str = 'POST'
    
    __api_delayed = 'https://query1.finance.yahoo.com/'
    __api = 'https://query2.finance.yahoo.com/'

    def __init__(self, lang:str='es-ES', verbose:bool=False) -> None:

        self.lang: dict = {
            'lang':lang,
            'region':lang.split('-')[-1],
        }
        self.verbose: bool = verbose

    def _request(self, url:str, headers:dict=None, params:dict=None, method:Method=Method.GET) -> requests.Response:

        if headers == None:
            headers = self._random_header()
        else:
            headers = {**self._random_header(), **headers}
            
        if params != None:
            params = {**params, **self.lang}
        
        if method == self.Method.GET:
            return requests.get(url, params=params, headers=headers)
        elif method == self.Method.POST:
            return requests.post(url, data=params, headers=headers)
        else:
            raise ValueError('Not a valid request method.')

    def searchText(self, text:str) -> str: 
        
        url = f'{self.__api}v1/finance/search'
        params = {
            'q':text,
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
        
        return self._request(url=url, params=params).json()

    def getCompanyInfo(self, ticker:str, info:list=['assetProfile', 'secFilings']) -> dict:

        url = f'{self.__api}v10/finance/quoteSummary/{ticker}'
        headers = {
            'host': 'query2.finance.yahoo.com',
            'origin': 'https://finance.yahoo.com',
            'cookie': 'A1=d=AQABBDP8ImQCEGphNhsXE3j7s4l9ziK1mJMFEgEBCAF70GX9Zdwr0iMA_eMBAAcILPwiZMBYI28&S=AQAAApVQ27mmHj84pi0oRFohDHI;'
        }
        params = {
            'formatted': 'true', 
            'crumb': 'IHtSUBEG..D', 
            'modules': ','.join(info),
            'corsDomain': 'finance.yahoo.com'
        }

        return self._request(url=url, headers=headers, params=params).json()
    
    def getDataAvailable(self) -> list:
        return ['longName', 'shortName', 'regularMarketPrice', 'regularMarketChange', 'regularMarketChangePercent', 'messageBoardId', 'marketCap', 'underlyingSymbol', 'underlyingExchangeSymbol', 'headSymbolAsString', 'regularMarketVolume', 'uuid', 'regularMarketOpen', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'toCurrency', 'fromCurrency', 'toExchange', 'fromExchange', 'corporateActions']
    
    def getQuote(self, ticker:str, data:list=['longName', 'regularMarketPrice', 'underlyingSymbol', 'fullExchangeName']) -> dict:

        url = f'{self.__api_delayed}v7/finance/quote'
        headers = {
            'host': 'query2.finance.yahoo.com',
            'origin': 'https://finance.yahoo.com',
            'cookie': 'A1=d=AQABBDP8ImQCEGphNhsXE3j7s4l9ziK1mJMFEgEBCAF70GX9Zdwr0iMA_eMBAAcILPwiZMBYI28&S=AQAAApVQ27mmHj84pi0oRFohDHI;'
        }
        params = {
            'formatted': 'true', 
            'crumb': 'IHtSUBEG..D', 
            'symbols': ticker, 
            'fields': ','.join(data), 
            'corsDomain': 'finance.yahoo.com'
        }

        return self._request(url=url, headers=headers, params=params).json()

    def getAvailableFinancials(self) -> list:
        return ['incomeStatementHistory', 'cashflowStatementHistory', 'balanceSheetHistory', 'incomeStatementHistoryQuarterly', 'cashflowStatementHistoryQuarterly', 'balanceSheetHistoryQuarterly']
    
    def getFinancials(self, ticker:str, financials:list=['incomeStatementHistory', 'incomeStatementHistoryQuarterly']) -> dict:

        url = f'{self.__api}v10/finance/quoteSummary/{ticker}'
        headers = {
            'host': 'query2.finance.yahoo.com',
            'origin': 'https://finance.yahoo.com',
            'cookie': 'A1=d=AQABBDP8ImQCEGphNhsXE3j7s4l9ziK1mJMFEgEBCAF70GX9Zdwr0iMA_eMBAAcILPwiZMBYI28&S=AQAAApVQ27mmHj84pi0oRFohDHI;'
        }
        params = {
            'formatted': True,
            'crumb': 'IHtSUBEG..D',
            'modules': ','.join(financials),
            'corsDomain': 'finance.yahoo.com',
        }
        
        return self._request(url=url, headers=headers, params=params).json()
    
    def getAvailableFundamentals(self) -> list:

        return ['annualTreasurySharesNumber', 'trailingTreasurySharesNumber', 'annualPreferredSharesNumber', 'trailingPreferredSharesNumber', 'annualOrdinarySharesNumber', 'trailingOrdinarySharesNumber', 'annualShareIssued', 'trailingShareIssued', 'annualNetDebt', 'trailingNetDebt', 'annualTotalDebt', 'trailingTotalDebt', 'annualTangibleBookValue', 'trailingTangibleBookValue', 'annualInvestedCapital', 'trailingInvestedCapital', 'annualWorkingCapital', 'trailingWorkingCapital', 'annualNetTangibleAssets', 'trailingNetTangibleAssets', 'annualCapitalLeaseObligations', 'trailingCapitalLeaseObligations', 'annualCommonStockEquity', 'trailingCommonStockEquity', 'annualPreferredStockEquity', 'trailingPreferredStockEquity', 'annualTotalCapitalization', 'trailingTotalCapitalization', 'annualTotalEquityGrossMinorityInterest', 'trailingTotalEquityGrossMinorityInterest', 'annualMinorityInterest', 'trailingMinorityInterest', 'annualStockholdersEquity', 'trailingStockholdersEquity', 'annualOtherEquityInterest', 'trailingOtherEquityInterest', 'annualGainsLossesNotAffectingRetainedEarnings', 'trailingGainsLossesNotAffectingRetainedEarnings', 'annualOtherEquityAdjustments', 'trailingOtherEquityAdjustments', 'annualFixedAssetsRevaluationReserve', 'trailingFixedAssetsRevaluationReserve', 'annualForeignCurrencyTranslationAdjustments', 'trailingForeignCurrencyTranslationAdjustments', 'annualMinimumPensionLiabilities', 'trailingMinimumPensionLiabilities', 'annualUnrealizedGainLoss', 'trailingUnrealizedGainLoss', 'annualTreasuryStock', 'trailingTreasuryStock', 'annualRetainedEarnings', 'trailingRetainedEarnings', 'annualAdditionalPaidInCapital', 'trailingAdditionalPaidInCapital', 'annualCapitalStock', 'trailingCapitalStock', 'annualOtherCapitalStock', 'trailingOtherCapitalStock', 'annualCommonStock', 'trailingCommonStock', 'annualPreferredStock', 'trailingPreferredStock', 'annualTotalPartnershipCapital', 'trailingTotalPartnershipCapital', 'annualGeneralPartnershipCapital', 'trailingGeneralPartnershipCapital', 'annualLimitedPartnershipCapital', 'trailingLimitedPartnershipCapital', 'annualTotalLiabilitiesNetMinorityInterest', 'trailingTotalLiabilitiesNetMinorityInterest', 'annualTotalNonCurrentLiabilitiesNetMinorityInterest', 'trailingTotalNonCurrentLiabilitiesNetMinorityInterest', 'annualOtherNonCurrentLiabilities', 'trailingOtherNonCurrentLiabilities', 'annualLiabilitiesHeldforSaleNonCurrent', 'trailingLiabilitiesHeldforSaleNonCurrent', 'annualRestrictedCommonStock', 'trailingRestrictedCommonStock', 'annualPreferredSecuritiesOutsideStockEquity', 'trailingPreferredSecuritiesOutsideStockEquity', 'annualDerivativeProductLiabilities', 'trailingDerivativeProductLiabilities', 'annualEmployeeBenefits', 'trailingEmployeeBenefits', 'annualNonCurrentPensionAndOtherPostretirementBenefitPlans', 'trailingNonCurrentPensionAndOtherPostretirementBenefitPlans', 'annualNonCurrentAccruedExpenses', 'trailingNonCurrentAccruedExpenses', 'annualDuetoRelatedPartiesNonCurrent', 'trailingDuetoRelatedPartiesNonCurrent', 'annualTradeandOtherPayablesNonCurrent', 'trailingTradeandOtherPayablesNonCurrent', 'annualNonCurrentDeferredLiabilities', 'trailingNonCurrentDeferredLiabilities', 'annualNonCurrentDeferredRevenue', 'trailingNonCurrentDeferredRevenue', 'annualNonCurrentDeferredTaxesLiabilities', 'trailingNonCurrentDeferredTaxesLiabilities', 'annualLongTermDebtAndCapitalLeaseObligation', 'trailingLongTermDebtAndCapitalLeaseObligation', 'annualLongTermCapitalLeaseObligation', 'trailingLongTermCapitalLeaseObligation', 'annualLongTermDebt', 'trailingLongTermDebt', 'annualLongTermProvisions', 'trailingLongTermProvisions', 'annualCurrentLiabilities', 'trailingCurrentLiabilities', 'annualOtherCurrentLiabilities', 'trailingOtherCurrentLiabilities', 'annualCurrentDeferredLiabilities', 'trailingCurrentDeferredLiabilities', 'annualCurrentDeferredRevenue', 'trailingCurrentDeferredRevenue', 'annualCurrentDeferredTaxesLiabilities', 'trailingCurrentDeferredTaxesLiabilities', 'annualCurrentDebtAndCapitalLeaseObligation', 'trailingCurrentDebtAndCapitalLeaseObligation', 'annualCurrentCapitalLeaseObligation', 'trailingCurrentCapitalLeaseObligation', 'annualCurrentDebt', 'trailingCurrentDebt', 'annualOtherCurrentBorrowings', 'trailingOtherCurrentBorrowings', 'annualLineOfCredit', 'trailingLineOfCredit', 'annualCommercialPaper', 'trailingCommercialPaper', 'annualCurrentNotesPayable', 'trailingCurrentNotesPayable', 'annualPensionandOtherPostRetirementBenefitPlansCurrent', 'trailingPensionandOtherPostRetirementBenefitPlansCurrent', 'annualCurrentProvisions', 'trailingCurrentProvisions', 'annualPayablesAndAccruedExpenses', 'trailingPayablesAndAccruedExpenses', 'annualCurrentAccruedExpenses', 'trailingCurrentAccruedExpenses', 'annualInterestPayable', 'trailingInterestPayable', 'annualPayables', 'trailingPayables', 'annualOtherPayable', 'trailingOtherPayable', 'annualDuetoRelatedPartiesCurrent', 'trailingDuetoRelatedPartiesCurrent', 'annualDividendsPayable', 'trailingDividendsPayable', 'annualTotalTaxPayable', 'trailingTotalTaxPayable', 'annualIncomeTaxPayable', 'trailingIncomeTaxPayable', 'annualAccountsPayable', 'trailingAccountsPayable', 'annualTotalAssets', 'trailingTotalAssets', 'annualTotalNonCurrentAssets', 'trailingTotalNonCurrentAssets', 'annualOtherNonCurrentAssets', 'trailingOtherNonCurrentAssets', 'annualDefinedPensionBenefit', 'trailingDefinedPensionBenefit', 'annualNonCurrentPrepaidAssets', 'trailingNonCurrentPrepaidAssets', 'annualNonCurrentDeferredAssets', 'trailingNonCurrentDeferredAssets', 'annualNonCurrentDeferredTaxesAssets', 'trailingNonCurrentDeferredTaxesAssets', 'annualDuefromRelatedPartiesNonCurrent', 'trailingDuefromRelatedPartiesNonCurrent', 'annualNonCurrentNoteReceivables', 'trailingNonCurrentNoteReceivables', 'annualNonCurrentAccountsReceivable', 'trailingNonCurrentAccountsReceivable', 'annualFinancialAssets', 'trailingFinancialAssets', 'annualInvestmentsAndAdvances', 'trailingInvestmentsAndAdvances', 'annualOtherInvestments', 'trailingOtherInvestments', 'annualInvestmentinFinancialAssets', 'trailingInvestmentinFinancialAssets', 'annualHeldToMaturitySecurities', 'trailingHeldToMaturitySecurities', 'annualAvailableForSaleSecurities', 'trailingAvailableForSaleSecurities', 'annualFinancialAssetsDesignatedasFairValueThroughProfitorLossTotal', 'trailingFinancialAssetsDesignatedasFairValueThroughProfitorLossTotal', 'annualTradingSecurities', 'trailingTradingSecurities', 'annualLongTermEquityInvestment', 'trailingLongTermEquityInvestment', 'annualInvestmentsinJointVenturesatCost', 'trailingInvestmentsinJointVenturesatCost', 'annualInvestmentsInOtherVenturesUnderEquityMethod', 'trailingInvestmentsInOtherVenturesUnderEquityMethod', 'annualInvestmentsinAssociatesatCost', 'trailingInvestmentsinAssociatesatCost', 'annualInvestmentsinSubsidiariesatCost', 'trailingInvestmentsinSubsidiariesatCost', 'annualInvestmentProperties', 'trailingInvestmentProperties', 'annualGoodwillAndOtherIntangibleAssets', 'trailingGoodwillAndOtherIntangibleAssets', 'annualOtherIntangibleAssets', 'trailingOtherIntangibleAssets', 'annualGoodwill', 'trailingGoodwill', 'annualNetPPE', 'trailingNetPPE', 'annualAccumulatedDepreciation', 'trailingAccumulatedDepreciation', 'annualGrossPPE', 'trailingGrossPPE', 'annualLeases', 'trailingLeases', 'annualConstructionInProgress', 'trailingConstructionInProgress', 'annualOtherProperties', 'trailingOtherProperties', 'annualMachineryFurnitureEquipment', 'trailingMachineryFurnitureEquipment', 'annualBuildingsAndImprovements', 'trailingBuildingsAndImprovements', 'annualLandAndImprovements', 'trailingLandAndImprovements', 'annualProperties', 'trailingProperties', 'annualCurrentAssets', 'trailingCurrentAssets', 'annualOtherCurrentAssets', 'trailingOtherCurrentAssets', 'annualHedgingAssetsCurrent', 'trailingHedgingAssetsCurrent', 'annualAssetsHeldForSaleCurrent', 'trailingAssetsHeldForSaleCurrent', 'annualCurrentDeferredAssets', 'trailingCurrentDeferredAssets', 'annualCurrentDeferredTaxesAssets', 'trailingCurrentDeferredTaxesAssets', 'annualRestrictedCash', 'trailingRestrictedCash', 'annualPrepaidAssets', 'trailingPrepaidAssets', 'annualInventory', 'trailingInventory', 'annualInventoriesAdjustmentsAllowances', 'trailingInventoriesAdjustmentsAllowances', 'annualOtherInventories', 'trailingOtherInventories', 'annualFinishedGoods', 'trailingFinishedGoods', 'annualWorkInProcess', 'trailingWorkInProcess', 'annualRawMaterials', 'trailingRawMaterials', 'annualReceivables', 'trailingReceivables', 'annualReceivablesAdjustmentsAllowances', 'trailingReceivablesAdjustmentsAllowances', 'annualOtherReceivables', 'trailingOtherReceivables', 'annualDuefromRelatedPartiesCurrent', 'trailingDuefromRelatedPartiesCurrent', 'annualTaxesReceivable', 'trailingTaxesReceivable', 'annualAccruedInterestReceivable', 'trailingAccruedInterestReceivable', 'annualNotesReceivable', 'trailingNotesReceivable', 'annualLoansReceivable', 'trailingLoansReceivable', 'annualAccountsReceivable', 'trailingAccountsReceivable', 'annualAllowanceForDoubtfulAccountsReceivable', 'trailingAllowanceForDoubtfulAccountsReceivable', 'annualGrossAccountsReceivable', 'trailingGrossAccountsReceivable', 'annualCashCashEquivalentsAndShortTermInvestments', 'trailingCashCashEquivalentsAndShortTermInvestments', 'annualOtherShortTermInvestments', 'trailingOtherShortTermInvestments', 'annualCashAndCashEquivalents', 'trailingCashAndCashEquivalents', 'annualCashEquivalents', 'trailingCashEquivalents', 'annualCashFinancial', 'trailingCashFinancial']

    def getFundamentalTimeseries(self, ticker:str, fundamentals:list=['annualTotalAssets', 'annualTotalLiabilitiesNetMinorityInterest']) -> dict:
        
        url = f'{self.__api_delayed}ws/fundamentals-timeseries/v1/finance/timeseries/{ticker}'

        params = {
            'symbol': ticker, 
            'padTimeSeries': 'true', 
            'type': ','.join(fundamentals),
            'merge': 'false',
            'period1': '493590046',
            'period2': '1708081300',
            'corsDomain': 'finance.yahoo.com'
        }
        headers = {
            'host': 'query2.finance.yahoo.com',
            'origin': 'https://finance.yahoo.com',
            'cookie': 'A1=d=AQABBDP8ImQCEGphNhsXE3j7s4l9ziK1mJMFEgEBCAF70GX9Zdwr0iMA_eMBAAcILPwiZMBYI28&S=AQAAApVQ27mmHj84pi0oRFohDHI;'
        }
        
        return self._request(url=url, headers=headers, params=params).json()

    def getKPI(self, ticker:str) -> dict:

        url = f'https://finance.yahoo.com/quote/{ticker}?.tsrc=fin-srch'
        html = BeautifulSoup(self._request(url=url).content, 'html.parser')

        return {
            'Logotype': '',
            'BPA': html.find('td', attrs={'data-test': 'EPS_RATIO-value'}).get_text(), # EPS
            'PER': html.find('td', attrs={'data-test': 'PE_RATIO-value'}).get_text(),
            'BETA': html.find('td', attrs={'data-test': 'BETA_5Y-value'}).get_text(),
        }

if __name__ == '__main__':
    
    text: str = 'aapl'
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
