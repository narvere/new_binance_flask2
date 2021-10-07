from flask import render_template, request
from funcs import getting_data_from_binance, pairs_info_from_binance
from dbs import AllTickers, db, DbsUpdateTime, AllTickersUpdateTime, TickersInfoUpdateTime, Assets, \
    coinInfotrades
from funcs import read_all_pairs, coin_shown_engine, count_of_coins, all_tradable_pairs, db_updating_time
from binance_info import client
import time


async def info_tickers():
    pairs_info_from_binance()
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    # print(my_assets)
    tickers_number = count_of_coins(AllTickers)

    TickersInfoUpdateTime.query.delete()
    times1 = db_updating_time()
    t = TickersInfoUpdateTime(tickers_info_table_time_upd=times1)
    db.session.add(t)
    db.session.commit()

    times, times_a, times_all = last_update_time()

    template_context = dict(
        my_assets=my_assets,
        super_total_usd=super_total_usd,
        super_total_eur=super_total_eur,
        number=number,
        tickers_number=tickers_number,
        times=times,
        times_all=times_all,
        times_a=times_a,
    )
    return render_template('index.html', **template_context)


# def ticker_info(ticker):
#     # all_pairs_info = db.session.query(PairsInfo).filter(
#     #     PairsInfo.baseAsset.in_([ticker])).order_by(PairsInfo.symbol).all()
#     all_pairs_info = db.session.query(coinInfotrades).filter(
#         coinInfotrades.baseAsset.in_([ticker])).order_by(db.desc(coinInfotrades.time_last_trades)).all()
#     # first_pairs_info = db.session.query(coinInfotrades).filter(
#     #     coinInfotrades.baseAsset.in_([ticker])).order_by(db.desc(coinInfotrades.time_last_trades)).first()
#     return all_pairs_info, first_pairs_info


# @app.route('/coin/<coin_name>/')
def coin(coin_name):
    print("def coin(coin_name)")
    # мзывает данные моей монеты
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    # мзывает данные последнего обновления
    times, times_a, times_all = last_update_time()
    # мои торговые пары
    ticker_i, first_pairs_info = my_trade_pairs(coin_name)

    template_context = dict(
        coin_name=coin_name,
        my_assets=my_assets,
        ticker_i=ticker_i,
        number=number,
        super_total_eur=super_total_eur,
        super_total_usd=super_total_usd,
        times=times,
        times_a=times_a,
        times_all=times_all,
        first_pairs_info=first_pairs_info,
    )

    return render_template('my_coin.html', **template_context)


def my_trade_pairs(coin_name):
    print("def my_trade_pairs(coin_name):")
    # ticker_i = ticker_info(coin_name)
    ticker_i = db.session.query(coinInfotrades).filter(
        coinInfotrades.baseAsset.in_([coin_name])).order_by(db.desc(coinInfotrades.time_last_trades)).all()
    first_pairs_info = db.session.query(coinInfotrades).filter(
        coinInfotrades.baseAsset.in_([coin_name])).order_by(db.desc(coinInfotrades.time_last_trades)).first()
    # print(ticker_i.symbol)
    # my_last_trades("MBOXUSDT")
    # for i in ticker_i:
    #     # print(i.symbol)
    #     all_pairs_info = db.session.query(coinInfotrades).filter(
    #         coinInfotrades.baseAsset == i.symbol).order_by(coinInfotrades.baseAsset).all()
    #     # print(all_pairs_info)
    return ticker_i, first_pairs_info


# @app.route('/all_usdt/', methods=['POST', 'GET'])
async def all_usdt():
    return "OK usdt"


# @app.route('/get_all_pairs/', methods=['POST', 'GET'])
def get_all_pairs():
    all_tradable_pairs(client)
    all_pairs_get, all_pairs_count = read_all_pairs()

    AllTickersUpdateTime.query.delete()
    times1 = db_updating_time()
    t = AllTickersUpdateTime(alltickers_table_time_upd=times1)
    db.session.add(t)
    db.session.commit()

    times, times_a, times_all = last_update_time()

    return render_template(
        'all_pairs.html',
        all_pairs=all_pairs_get,
        times=times,
        times_all=times_all,
        times_a=times_a,
        all_pairs_count=all_pairs_count,
    )


def last_update_time():
    times = DbsUpdateTime.query.all()
    times_all = AllTickersUpdateTime.query.all()
    times_a = TickersInfoUpdateTime.query.all()
    return times, times_a, times_all


# @app.route('/')

# def time_count(func):
#     def answer():
#         t0 = time.time()
#         times = func()
#         tt = time.time() - t0
#         print(time.time() - t0)
#         return times, tt
#
#     return answer


# @time_count
def base():
    t0 = time.time()
    times, times_a, times_all = last_update_time()
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    tickers_number = count_of_coins(AllTickers)
    tt = time.time() - t0
    template_context = dict(
        my_assets=my_assets,
        super_total_usd=super_total_usd,
        super_total_eur=super_total_eur,
        number=number,
        tickers_number=tickers_number,
        times=times,
        times_all=times_all,
        times_a=times_a,
        tt=tt
    )
    return render_template('index.html', **template_context)


# @app.route('/my_coins/', methods=['POST', 'GET'])
def my_coins():
    now = time.time()
    # получаю все данные с бинанса
    getting_data_from_binance()
    Assets.query.filter(Assets.update_time < now).delete()
    Assets.query.filter(Assets.update_time == None).delete()
    # удаляю время последнего апдейта
    DbsUpdateTime.query.delete()
    # получаю время последнего апдейта
    times1 = db_updating_time()
    # записываю время последнего апдейта
    t = DbsUpdateTime(assets_table_time_upd=times1)
    db.session.add(t)
    db.session.commit()
    # принимаю время обновления из базы для вывода на страницу
    times, times_a, times_all = last_update_time()
    # принимаю количество тикеров
    tickers_number = count_of_coins(AllTickers)
    # принимаю данные для вывода на страницу
    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    # print(super_total_eur)
    template_context = dict(
        my_assets=my_assets,
        super_total_usd=super_total_usd,
        super_total_eur=super_total_eur,
        number=number,
        tickers_number=tickers_number,
        times=times,
        times_all=times_all,
        times_a=times_a,
    )
    return render_template('index.html', **template_context)


# @app.route('/all_pairs/', methods=['POST', 'GET'])
async def all_pairs():
    times, times_a, times_all = last_update_time()

    my_assets, number, super_total_eur, super_total_usd = coin_shown_engine()
    tickers_number = count_of_coins(AllTickers)
    all_pairs_binance, all_pairs_count = read_all_pairs()
    template_context = dict(
        all_pairs=all_pairs_binance,
        super_total_usd=super_total_usd,
        super_total_eur=super_total_eur,
        number=number,
        tickers_number=tickers_number,
        times=times,
        times_all=times_all,
        times_a=times_a,
        all_pairs_count=all_pairs_count,
    )
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
