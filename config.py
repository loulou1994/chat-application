import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = "81d4c0b81c81fba77a4e3b8a39365772"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or f'sqlite:///{os.path.join(basedir, 'app.db')}'
