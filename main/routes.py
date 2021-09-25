import pytz
from flask import render_template
from get_data_from_binance import getting_data_from_binance
from dbs import AllTickers, app
from funcs import read_all_pairs, coin_shown_engine, count_of_coins, all_tradable_pairs
from binance_info import client


# @app.route('/coin/<coin_name>/')
def coin(coin_name):
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    return render_template('my_coin.html', coin_name=coin_name, my_assets=my_assets)


# @app.route('/all_usdt/', methods=['POST', 'GET'])
async def all_usdt():
    return "OK usdt"


# @app.route('/get_all_pairs/', methods=['POST', 'GET'])
async def get_all_pairs():
    all_tradable_pairs(client)
    all_pairs_get = read_all_pairs()

    return render_template('all_pairs.html', all_pairs=all_pairs_get)


# @app.route('/')
def base():
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    print(my_assets)
    tickers_number = count_of_coins(AllTickers)
    return render_template('index.html', my_assets=my_assets, super_total_usd=super_total_usd,
                           super_total_eur=super_total_eur, number=number, tickers_number=tickers_number)


# @app.route('/my_coins/', methods=['POST', 'GET'])
def my_coins():
    getting_data_from_binance()
    tickers_number = count_of_coins(AllTickers)
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    print(my_assets)
    return render_template('index.html', my_assets=my_assets, super_total_usd=super_total_usd,
                           super_total_eur=super_total_eur, number=number, tickers_number=tickers_number, )


@app.route('/all_pairs/', methods=['POST', 'GET'])
async def all_pairs():
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    tickers_number = count_of_coins(AllTickers)
    all_pairs = read_all_pairs()
    return render_template('all_pairs.html', all_pairs=all_pairs, super_total_usd=super_total_usd,
                           super_total_eur=super_total_eur, number=number, tickers_number=tickers_number, )
