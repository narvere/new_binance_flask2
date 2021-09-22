from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# pip install flask-sqlalchemy
# from dbs import db
# db.create_all()

# .\venv\Scripts\activate
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///binance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Assets(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    asset = db.Column(db.String(50), nullable=False)
    free = db.Column(db.Float, unique=False, nullable=True)
    locked = db.Column(db.Float, unique=False, nullable=True)
    total_usd = db.Column(db.Float, unique=False, nullable=True)
    total_eur = db.Column(db.Float, unique=False, nullable=True)
    recommendatsion = db.Column(db.String(50), nullable=False)

    def __init__(self, asset, free, locked, total_usd, total_eur, recommendatsion):
        self.asset = asset
        self.free = free
        self.locked = locked
        self.total_usd = total_usd
        self.total_eur = total_eur
        self.recommendatsion = recommendatsion

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


class all_tickers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self):
        return '<Ticker %r>' % self.ticker


class usdt_tickers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), nullable=False, unique=True)


def __repr__(self):
    return '<Ticker %r>' % self.ticker
