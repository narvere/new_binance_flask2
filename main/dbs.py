from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# # set FLASK_APP=dbs.py
# flask db init
# flask db migrate -m "Initial migration."
# flask db upgrade

# pip install flask-sqlalchemy
# from dbs import db
# db.create_all()

# .\venv\Scripts\activate
db = SQLAlchemy()

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///binance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)


class Assets(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    asset = db.Column(db.String(50), nullable=False)
    free = db.Column(db.Float, unique=False, nullable=True)
    locked = db.Column(db.Float, unique=False, nullable=True)
    total_usd = db.Column(db.Float, unique=False, nullable=True)
    total_eur = db.Column(db.Float, unique=False, nullable=True)
    recommendatsion = db.Column(db.String(50), nullable=True)
    recommendatsion_d1 = db.Column(db.String(50), nullable=True)

    def __init__(self, asset, free, locked, total_usd, total_eur, recommendatsion, recommendatsion_d1):
        self.asset = asset
        self.free = free
        self.locked = locked
        self.total_usd = total_usd
        self.total_eur = total_eur
        self.recommendatsion = recommendatsion
        self.recommendatsion_d1 = recommendatsion_d1

    def __repr__(self):
        return '<Assets %r>' % self.asset


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, unique=False, nullable=True)
    origQty = db.Column(db.Float, unique=False, nullable=True)
    executedQty = db.Column(db.Float, unique=False, nullable=True)
    order_type = db.Column(db.String(50), unique=False, nullable=True)
    side = db.Column(db.String(50), unique=False, nullable=True)
    stopPrice = db.Column(db.Float, unique=False, nullable=True)
    time = db.Column(db.String(50), unique=False, nullable=True)

    def __repr__(self):
        return '<Orders %r>' % self.symbol


class AllTickers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), nullable=False, unique=True)
    recommendatsion = db.Column(db.String(50), nullable=True)
    recommendatsion_all_day = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return '<Ticker %r>' % self.ticker


class UsdtTickers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), nullable=False, unique=True)


def __repr__(self):
    return '<Ticker %r>' % self.ticker
