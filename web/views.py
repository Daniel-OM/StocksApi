
import datetime as dt
import sqlite3
import json
import sys

import numpy as np
import pandas as pd

sys.path.append('..')

from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, flash, redirect, render_template, request, url_for
    
    

# checKey = lambda k, dic: dic[k] if k in dic else None
def checKey(k, dic):
    return dic[k] if k in dic else None

# entityToDict = lambda entity, hidden_fields: {k: v for k, v in entity.__dict__.items() if k not in hidden_fields}
def entityToDict(entity, hidden_fields:list=[]) -> dict:
    
    return {k: v for k, v in entity.__dict__.items() if k not in hidden_fields}

views = Blueprint('views', __name__)

@views.route("/")
@views.route("/home")
def home() -> str:
    return render_template('home.html')

@views.route("/ticker", methods=["GET", "POST"])
def ticker_get():
    
    if request.method == 'POST':
        
        message = ''

        data = {k: v[0] if len(v) == 1 else v
            for k, v in request.form.to_dict(flat=False).items() if v or v > 0 or len(v) > 0}
        
        # if data['company'] != '':
        #     pass
        # elif data['symbol'] != '':
        #     pass
        # else:
        #     message = 'ERROR: There was an error while runing the search! There are no company or symbol.'
        
        data = {
            'Ticker': 'AAPL',
            'Company': 'Apple',
            'Logotype': '',
            'Exchange': 'NASDAQ',
            'Contry': 'United States',
            'Sector': 'Technology',
            'Sub-Sector': 'Technology consumers',
            'Employees': 161000,
            'Price': {'Value': 188.85, 'Time': '04:00'},
            'BPA': 6.16, # EPS
            'PER': 29.32,
            'BETA': 1.31,
            'Revenue': {'TTM': 385706000, 'Last':383285000},
            'Net-Earnings': {'TTM':100913000, 'Last':96995000},
            'Assets': 352583000,
            'Liabilities': 290437000,
            'Description': 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod. It also provides AppleCare support and cloud services; and operates various platforms, including the App Store that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts. In addition, the company offers various services, such as Apple Arcade, a game subscription service; Apple Fitness+, a personalized fitness service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It distributes third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was founded in 1976 and is headquartered in Cupertino, California.'
        }
        
        return render_template('home.html', data=data, message=message)
    else:
        return 'You are UNAUTHORIZED to edit this vehicle!'

@views.route("/about")
def about() -> str:
    return render_template('about.html')
