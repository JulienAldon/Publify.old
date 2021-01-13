import os
basedir = os.path.abspath(os.path.dirname(__file__))

CLIENTKEY=u'8849b50e64c547caa0baef44c72c5d34'
CLIENTSECRET=u'197ea6bb66ed46c58e9a703f7d1eec90'
SECRET_KEY = "baise bien ta maman"
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://guest:guest@database:5432/publify
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False