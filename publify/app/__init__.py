#!/usr/bin/env python3
from flask import Flask
# from config import Config
# from app import models
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
app.config.from_pyfile('config.py')
cors = CORS(app, 
    origins="http://publify.aldon.info", 
    allow_headers=[
        "Content-Type", "Authorization", "Access-Control-Allow-Credentials"
    ],
    supports_credentials=True
)
app.config['CORS_HEADERS'] = 'Content-Type'

db = SQLAlchemy(app)


from app import api, models