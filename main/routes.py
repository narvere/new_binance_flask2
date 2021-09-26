from flask import render_template, request
from get_data_from_binance import getting_data_from_binance, pairs_info_from_binance, a_price
from dbs import AllTickers, app, PairsInfo, db
from funcs import read_all_pairs, coin_shown_engine, count_of_coins, all_tradable_pairs
from binance_info import client


async def info_tickers():
    pairs_info_from_binance()
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    print(my_assets)
    tickers_number = count_of_coins(AllTickers)
    template_context = dict(my_assets=my_assets, super_total_usd=super_total_usd,
                            super_total_eur=super_total_eur, number=number, tickers_number=tickers_number)
    return render_template('index.html', **template_context)


def ticker_info(ticker):
    all_pairs_info = db.session.query(PairsInfo).filter(
        PairsInfo.baseAsset.in_([ticker])).order_by(PairsInfo.symbol).all()
    return all_pairs_info


# @app.route('/coin/<coin_name>/')
def coin(coin_name):
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    ticker_i = str(ticker_info(coin_name))
    price = a_price(ticker_i)
    template_context = dict(coin_name=coin_name, my_assets=my_assets, ticker_i=ticker_i, price=price)

    return render_template('my_coin.html', **template_context)


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
    template_context = dict(my_assets=my_assets, super_total_usd=super_total_usd,
                            super_total_eur=super_total_eur, number=number, tickers_number=tickers_number)
    return render_template('index.html', **template_context)


# @app.route('/my_coins/', methods=['POST', 'GET'])
def my_coins():
    getting_data_from_binance()
    tickers_number = count_of_coins(AllTickers)
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    print(my_assets)
    template_context = dict(my_assets=my_assets, super_total_usd=super_total_usd,
                            super_total_eur=super_total_eur, number=number, tickers_number=tickers_number, )
    return render_template('index.html', **template_context)


# @app.route('/all_pairs/', methods=['POST', 'GET'])
async def all_pairs():
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    tickers_number = count_of_coins(AllTickers)
    all_pairs_binance = read_all_pairs()
    template_context = dict(all_pairs=all_pairs_binance, super_total_usd=super_total_usd,
                            super_total_eur=super_total_eur, number=number, tickers_number=tickers_number, )
    return render_template('all_pairs.html', **template_context)


# @app.route('/login/', methods=['post', 'get'])
def login():
    global username, password
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным формы
        password = request.form.get('password')

    if username == 'root' and password == 'pass':
        message = "Correct username and password"
    else:
        message = "Wrong username or password"

    return render_template('login.html', message=message)
