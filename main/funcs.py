from dbs import all_tickers
from dbs import Assets, db
from time import time
from tradingview_ta import TA_Handler, Interval, Exchange


def trading_view_recommendation(coin):
    tesla = TA_Handler(
        symbol=f"{coin}USDT",
        screener="CRYPTO",
        exchange="BINANCE",
        interval=Interval.INTERVAL_4_HOURS
    )
    recommend = tesla.get_analysis().summary.get('RECOMMENDATION')
    return recommend


def trading_view_recommendation_all(coin):
    tesla = TA_Handler(
        symbol=f"{coin}",
        screener="CRYPTO",
        exchange="BINANCE",
        interval=Interval.INTERVAL_4_HOURS
    )
    recommend = tesla.get_analysis().summary.get('RECOMMENDATION')
    return recommend


def count_of_coins(xxx):
    numbers = db.session.query(db.func.count(xxx.id))
    for nr in numbers:
        for number in nr:
            return number


def currency(asset):
    if asset == 'total_usd':
        super_total_usds = db.session.query(db.func.sum(Assets.total_usd))
    else:
        super_total_usds = db.session.query(db.func.sum(Assets.total_eur))
    for super_total_usd in super_total_usds:
        for i in super_total_usd:
            return i


def coin_shown_engine():
    t0 = time()
    my_assets = Assets.query.order_by(-Assets.total_usd).all()
    print(type(my_assets))
    # recommend = trading_view_recommendation('BTC')
    super_total_usd = currency('total_usd')
    super_total_eur = currency('total_eur')
    try:
        super_total_usd = round(super_total_usd, 2)
        super_total_eur = round(super_total_eur, 2)
    except:
        pass
    number = count_of_coins(Assets)
    tt = t0 - time()
    print(tt)
    return my_assets, number, super_total_eur, super_total_usd


def read_all_pairs():
    all_pairs = all_tickers.query.order_by(-all_tickers.ticker).all()
    return all_pairs


def all_tradable_pairs(client):
    # t0 = time()
    global recommendatsion_all
    tickers1 = client.get_orderbook_tickers()
    all_tickers.query.delete()
    count = 0

    for ticker in tickers1[:7]:
        bidPrice = float(ticker.get('bidPrice'))
        if bidPrice > 0:
            count += 1
            symbol = ticker.get('symbol')
            exists = db.session.query(all_tickers.id).filter_by(ticker=symbol).first() is not None
            if not exists:
                recommendatsion_all = trading_view_recommendation_all(symbol)
                admin2 = all_tickers(ticker=symbol, recommendatsion=recommendatsion_all)
                db.session.add(admin2)
                db.session.commit()
            else:
                admin = all_tickers.query.filter_by(ticker=symbol).first()
                admin.ticker = symbol
                # admin.recommendatsion_all = trading_view_recommendation_all(symbol)
                db.session.add(admin)
                db.session.commit()
                print('11111111')
            print(count, symbol)
    # tt = time() - t0
    # print(tt)
