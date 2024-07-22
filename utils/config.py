import os

class Config:
    db_host = os.environ.get('DB_HOST') or 'localhost'
    db_user = os.environ.get('DB_USER') or 'dbadmin'
    db_pass = os.environ.get('DB_PASS') or 'dbadmin-pass'
    db_name = 'cityinfo'
    SQLALCHEMY_DATABASE_URI = f'mysql://{db_user}:{db_pass}@{db_host}/{db_name}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
