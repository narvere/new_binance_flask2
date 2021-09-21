from dbs import Assets, Orders, db, app
import pytz
from flask import render_template
from time import time
from get_data_from_binance import getting_data_from_binance, client
from acink import mains, Binance_tickers
from dbs import all_tickers
import asyncio
from sqlalchemy import create_engine

# pip install flask[async]
# pip install flask
# pip install pytz
zone_ee = pytz.timezone('Europe/Tallinn')

# engine = create_engine('sqlite:///binance2.db')
# conn = engine.connect()

def all_tradable_pairs(client):
    # t0 = time()
    tickers1 = client.get_orderbook_tickers()
    all_tickers.query.delete()
    count = 0

    for ticker in tickers1:
        bidPrice = float(ticker.get('bidPrice'))
        if bidPrice > 0:
            count += 1
            symbol = ticker.get('symbol')
            exists = db.session.query(all_tickers.id).filter_by(ticker=symbol).first() is not None
            if not exists:
                admin2 = all_tickers(ticker=symbol)
                db.session.add(admin2)
                db.session.commit()
            else:
                admin = all_tickers.query.filter_by(ticker=symbol).first()
                admin.ticker = symbol
                db.session.add(admin)
                db.session.commit()
            print(count, symbol)
    # tt = time() - t0
    # print(tt)

def read_all_pairs():
    all_pairs = all_tickers.query.order_by(-all_tickers.ticker).all()
    return all_pairs


# @app.route('/')
# class Base():
#     def __init__(self, my_assets, number, super_total_eur, super_total_usd):
#         self.my_assets = my_assets
#         self.number = number
#         self.super_total_eur = super_total_eur
#         self.super_total_usd = super_total_usd
#
#     def base(self):
#         self.my_assets, self.number, self.super_total_eur, self.super_total_usd = self.coin_shown_engine()
#         return render_template('index.html', my_assets=self.my_assets, super_total_usd=self.super_total_usd,
#                                super_total_eur=self.super_total_eur, number=self.number)
@app.route('/')
def base():
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    tickers_number = count_of_coins(all_tickers)
    return render_template('index.html', my_assets=my_assets, super_total_usd=super_total_usd,
                           super_total_eur=super_total_eur, number=number, tickers_number=tickers_number)


@app.route('/my_coins/', methods=['POST', 'GET'])
def my_coins():
    getting_data_from_binance()
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    return render_template('index.html', my_assets=my_assets, super_total_usd=super_total_usd,
                           super_total_eur=super_total_eur, number=number)


@app.route('/all_pairs/', methods=['POST', 'GET'])
async def all_pairs():
    # all_tradable_pairs(client)
    all_pairs = read_all_pairs()

    return render_template('all_pairs.html', all_pairs=all_pairs)


@app.route('/all_usdt/', methods=['POST', 'GET'])
async def all_usdt():
    return "OK usdt"


@app.route('/coin/<coin_name>/')
def coin(coin_name):
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    return render_template('my_coin.html', coin_name=coin_name, my_assets=my_assets)


def coin_shown_engine():
    t0 = time()
    my_assets = Assets.query.order_by(-Assets.total_usd).all()
    super_total_usd = round(currency('total_usd'), 2)
    super_total_eur = round(currency('total_eur'), 2)
    number = count_of_coins(Assets)
    tt = t0 - time()
    print(tt)
    return my_assets, number, super_total_eur, super_total_usd


def currency(asset):
    if asset == 'total_usd':
        super_total_usds = db.session.query(db.func.sum(Assets.total_usd))
    else:
        super_total_usds = db.session.query(db.func.sum(Assets.total_eur))
    for super_total_usd in super_total_usds:
        for i in super_total_usd:
            return i


def count_of_coins(xxx):
    numbers = db.session.query(db.func.count(xxx.id))
    for nr in numbers:
        for number in nr:
            return number


if __name__ == '__main__':
    app.run(debug=True)
