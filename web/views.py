
import datetime as dt
import sqlite3
import json
import sys

import numpy as np
import pandas as pd

sys.path.append('..')

from flask import Blueprint, flash, redirect, render_template, request, url_for
    
from .scraper import getTickerData   

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
        
        if data['company'] != '':
            data = getTickerData(data['company'])
        elif data['symbol'] != '':
            data = getTickerData(data['symbol'])
        else:
            message = 'ERROR: There was an error while runing the search! There are no company or symbol.'
        
        
        return render_template('home.html', data=data, message=message)
    else:
        return 'You are UNAUTHORIZED to edit this vehicle!'

@views.route("/about")
def about() -> str:
    return render_template('about.html')
