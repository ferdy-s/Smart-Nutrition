import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = 'SECRET_KEY'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_OAUTH_CLIENT_ID = 'GOOGLE_CLIENT_ID'

    GOOGLE_OAUTH_CLIENT_SECRET = 'GOOGLE_CLIENT_SECRET'