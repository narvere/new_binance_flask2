from flask import render_template, request
from get_data_from_binance import getting_data_from_binance, pairs_info_from_binance, my_last_trades
from dbs import AllTickers, PairsInfo, db, DbsUpdateTime, AllTickersUpdateTime, TickersInfoUpdateTime
from funcs import read_all_pairs, coin_shown_engine, count_of_coins, all_tradable_pairs, db_updating_time
from binance_info import client


async def info_tickers():
    pairs_info_from_binance()
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    print(my_assets)
    tickers_number = count_of_coins(AllTickers)

    TickersInfoUpdateTime.query.delete()
    times1 = db_updating_time()
    t = TickersInfoUpdateTime(tickers_info_table_time_upd=times1)
    db.session.add(t)
    db.session.commit()

    times, times_a, times_all = last_update_time()

    template_context = dict(my_assets=my_assets, super_total_usd=super_total_usd,
                            super_total_eur=super_total_eur, number=number, tickers_number=tickers_number, times=times,
                            times_all=times_all, times_a=times_a)
    return render_template('index.html', **template_context)


def ticker_info(ticker):
    all_pairs_info = db.session.query(PairsInfo).filter(
        PairsInfo.baseAsset.in_([ticker])).order_by(PairsInfo.symbol).all()
    return all_pairs_info


# @app.route('/coin/<coin_name>/')
def coin(coin_name):
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    ticker_i = ticker_info(coin_name)
    my_last_trades("MBOXUSDT")
    # for i in ticker_i:
    #     # print(i.symbol)
    #     price = a_price(i.symbol)
    #     pairs_info = PairsInfo(symbol=i.symbol, test=price)
    #     db.session.add(pairs_info)
    #     db.session.commit()

    template_context = dict(coin_name=coin_name, my_assets=my_assets, ticker_i=ticker_i)

    return render_template('my_coin.html', **template_context)


# @app.route('/all_usdt/', methods=['POST', 'GET'])
async def all_usdt():
    return "OK usdt"


# @app.route('/get_all_pairs/', methods=['POST', 'GET'])
async def get_all_pairs():
    all_tradable_pairs(client)
    all_pairs_get = read_all_pairs()

    AllTickersUpdateTime.query.delete()
    times1 = db_updating_time()
    t = AllTickersUpdateTime(alltickers_table_time_upd=times1)
    db.session.add(t)
    db.session.commit()

    times, times_a, times_all = last_update_time()

    return render_template('all_pairs.html', all_pairs=all_pairs_get, times=times, times_all=times_all, times_a=times_a)


def last_update_time():
    times = DbsUpdateTime.query.all()
    times_all = AllTickersUpdateTime.query.all()
    times_a = TickersInfoUpdateTime.query.all()
    return times, times_a, times_all


# @app.route('/')
def base():
    times, times_a, times_all = last_update_time()

    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    print(my_assets)
    tickers_number = count_of_coins(AllTickers)
    template_context = dict(my_assets=my_assets, super_total_usd=super_total_usd,
                            super_total_eur=super_total_eur, number=number, tickers_number=tickers_number, times=times,
                            times_all=times_all, times_a=times_a)
    return render_template('index.html', **template_context)


# @app.route('/my_coins/', methods=['POST', 'GET'])
def my_coins():
    getting_data_from_binance()

    DbsUpdateTime.query.delete()
    times1 = db_updating_time()
    t = DbsUpdateTime(assets_table_time_upd=times1)
    db.session.add(t)
    db.session.commit()
    times, times_a, times_all = last_update_time()

    # Assets.query.delete()
    # db.session.commit()
    tickers_number = count_of_coins(AllTickers)
    my_assets, number, super_total_eur, super_total_usd, price = coin_shown_engine()
    print(my_assets)
    template_context = dict(my_assets=my_assets, super_total_usd=super_total_usd,
                            super_total_eur=super_total_eur, number=number, tickers_number=tickers_number, times=times,
                            times_all=times_all, times_a=times_a, price=price)
    return render_template('index.html', **template_context)


# @app.route('/all_pairs/', methods=['POST', 'GET'])
async def all_pairs():
    times, times_a, times_all = last_update_time()

    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    tickers_number = count_of_coins(AllTickers)
    all_pairs_binance = read_all_pairs()
    template_context = dict(all_pairs=all_pairs_binance, super_total_usd=super_total_usd,
                            super_total_eur=super_total_eur, number=number, tickers_number=tickers_number, times=times,
                            times_all=times_all, times_a=times_a)
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
