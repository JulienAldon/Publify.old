#!/usr/bin/env python3
from flask import Flask
# from config import Config
# from app import models
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app,
    origins=["publify.aldon.info"],
    resources=r"api/*",
    supports_credentials=True
)
app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy(app)

from app import api, models