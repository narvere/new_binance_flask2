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


class coinInfotrades(db.Model):
    __tablename__ = 'coinInfotrades'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50), unique=False, nullable=True)
    baseAsset = db.Column(db.String(50), unique=False, nullable=True)
    quoteAsset = db.Column(db.String(50), unique=False, nullable=True)
    current_price = db.Column(db.Float, unique=False, nullable=True)
    binance_id = db.Column(db.Integer, unique=True, nullable=True)
    orderId = db.Column(db.Integer, unique=False, nullable=True)
    time_last_trades = db.Column(db.String(50), unique=False, nullable=True)
    price = db.Column(db.Float, unique=False, nullable=True)
    qty = db.Column(db.Float, unique=False, nullable=True)
    quote_qty = db.Column(db.Float, unique=False, nullable=True)
    commis = db.Column(db.Float, unique=False, nullable=True)
    commisAsset = db.Column(db.String(20), unique=False, nullable=True)

    def __init__(self, symbol, baseAsset, quoteAsset, current_price, binance_id, orderId, time_last_trades, price, qty,
                 quote_qty, commis, commisAsset):
        self.symbol = symbol
        self.baseAsset = baseAsset
        self.quoteAsset = quoteAsset
        self.current_price = current_price
        self.binance_id = binance_id
        self.orderId = orderId
        self.time_last_trades = time_last_trades
        self.price = price
        self.qty = qty
        self.quote_qty = quote_qty
        self.commis = commis
        self.commisAsset = commisAsset

    def __repr__(self):
        return '<symbol %r>' % self.symbol


class myTrades(db.Model):
    __tablename__ = 'mytrades'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50), unique=False, nullable=True)
    binance_id = db.Column(db.Integer, unique=True, nullable=True)
    orderId = db.Column(db.Integer, unique=False, nullable=True)
    time_last_trades = db.Column(db.String(50), unique=False, nullable=True)
    price = db.Column(db.Float, unique=False, nullable=True)
    qty = db.Column(db.Float, unique=False, nullable=True)
    quote_qty = db.Column(db.Float, unique=False, nullable=True)
    commis = db.Column(db.Float, unique=False, nullable=True)
    commisAsset = db.Column(db.String(20), unique=False, nullable=True)

    def __init__(self, symbol, binance_id, orderId, time_last_trades, price, qty, quote_qty, commis, commisAsset):
        self.symbol = symbol
        self.binance_id = binance_id
        self.orderId = orderId
        self.time_last_trades = time_last_trades
        self.price = price
        self.qty = qty
        self.quote_qty = quote_qty
        self.commis = commis
        self.commisAsset = commisAsset

    def __repr__(self):
        return '<symbol %r>' % self.symbol


class DbsUpdateTime(db.Model):
    __tablename__ = 'dbupdatetime'
    id = db.Column(db.Integer, primary_key=True)
    assets_table_time_upd = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<symbol %r>' % self.assets_table_time_upd


class AllTickersUpdateTime(db.Model):
    __tablename__ = 'alltickerupdatetime'
    id = db.Column(db.Integer, primary_key=True)
    alltickers_table_time_upd = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<symbol %r>' % self.alltickers_table_time_upd


class TickersInfoUpdateTime(db.Model):
    __tablename__ = 'tickerinfoupdatetime'
    id = db.Column(db.Integer, primary_key=True)
    tickers_info_table_time_upd = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<time %r>' % self.tickers_info_table_time_upd


# class MyTrades(db.Model):
#     __tablename__ = 'my_trades'
#     id = db.Column(db.Integer, primary_key=True)
#     time_last_trades = db.Column(db.String(50), unique=False, nullable=True)
#     symbol = db.Column(db.String(50), nullable=False)
#     price = db.Column(db.String(50), unique=False, nullable=True)
#     qty = db.Column(db.String(50), unique=False, nullable=True)
#     quote_qty = db.Column(db.String(50), unique=False, nullable=True)
#     commis = db.Column(db.String(50), unique=False, nullable=True)
#     commisAsset = db.Column(db.String(50), unique=False, nullable=True)
#
#     def __init__(self, time_last_trades, symbol, price, qty, quote_qty, commis, commisAsset):
#         self.symbol = symbol
#         self.time_last_trades = time_last_trades
#         self.price = price
#         self.qty = qty
#         self.quote_qty = quote_qty
#         self.commis = commis
#         self.commisAsset = commisAsset
#
#     def __repr__(self):
#         return '<symbol %r>' % self.symbol


class PairsInfo(db.Model):
    __tablename__ = 'pairsinfo'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(50), nullable=False)
    baseAsset = db.Column(db.String(50), unique=False, nullable=True)
    quoteAsset = db.Column(db.String(50), unique=False, nullable=True)
    orderTypes = db.Column(db.String(500), unique=False, nullable=True)
    permissions = db.Column(db.String(500), unique=False, nullable=True)
    test = db.Column(db.String(500), unique=False, nullable=True)

    def __init__(self, symbol, baseAsset, quoteAsset, orderTypes, permissions, test):
        self.symbol = symbol
        self.baseAsset = baseAsset
        self.quoteAsset = quoteAsset
        self.orderTypes = orderTypes
        self.permissions = permissions
        self.test = test

    def __repr__(self):
        return '<symbol %r>' % self.symbol


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
    price = db.Column(db.Float, unique=False, nullable=True)
    update_time = db.Column(db.Float, unique=False, nullable=True)

    def __init__(self, asset, free, locked, total_usd, total_eur, recommendatsion, recommendatsion_d1, price,
                 update_time):
        self.asset = asset
        self.free = free
        self.locked = locked
        self.total_usd = total_usd
        self.total_eur = total_eur
        self.recommendatsion = recommendatsion
        self.recommendatsion_d1 = recommendatsion_d1
        self.price = price
        self.update_time = update_time

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
    all_pairs_info = db.Column(db.String, nullable=True)

    def __init__(self, ticker, recommendatsion, recommendatsion_all_day, all_pairs_info):
        self.ticker = ticker
        self.recommendatsion = recommendatsion
        self.recommendatsion_all_day = recommendatsion_all_day
        self.all_pairs_info = all_pairs_info

    def __repr__(self):
        return '<Ticker %r>' % self.ticker


class UsdtTickers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), nullable=False, unique=True)


def __repr__(self):
    return '<Ticker %r>' % self.ticker
