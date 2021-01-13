#!/usr/bin/env python3
from flask import Flask
# from config import Config
# from app import models
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
app.config.from_pyfile('config.py')
cors = CORS(app, CORS_ORIGINS=['publify.aldon.info'])
db = SQLAlchemy(app)


from app import api, models