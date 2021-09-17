from dbs import User, Orders, db, app
import pytz
from flask import render_template
from time import time
from get_data_from_binance import getting_data_from_binance

#pip install flask
#pip install pytz
zone_ee = pytz.timezone('Europe/Tallinn')


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
    return render_template('index.html', my_assets=my_assets, super_total_usd=super_total_usd,
                           super_total_eur=super_total_eur, number=number)


@app.route('/my_coins/', methods=['POST', 'GET'])
def my_coins():
    getting_data_from_binance()
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    return render_template('index.html', my_assets=my_assets, super_total_usd=super_total_usd,
                           super_total_eur=super_total_eur, number=number)


@app.route('/coin/<coin_name>/')
def coin(coin_name):
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    return render_template('my_coin.html', coin_name=coin_name, my_assets=my_assets)


#

def coin_shown_engine():
    t0 = time()
    my_assets = User.query.order_by(-User.total_usd).all()
    super_total_usd = round(currency('total_usd'), 2)
    super_total_eur = round(currency('total_eur'), 2)
    number = count_of_coins()
    tt = t0 - time()
    print(tt)
    return my_assets, number, super_total_eur, super_total_usd


def currency(asset):
    if asset == 'total_usd':
        super_total_usds = db.session.query(db.func.sum(User.total_usd))
    else:
        super_total_usds = db.session.query(db.func.sum(User.total_eur))
    for super_total_usd in super_total_usds:
        for i in super_total_usd:
            return i


def count_of_coins():
    numbers = db.session.query(db.func.count(User.asset))
    for nr in numbers:
        for number in nr:
            return number


if __name__ == '__main__':
    app.run(debug=True)
