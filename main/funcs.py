from dbs import db, Assets, AllTickers, myTrades
from time import time
from tradingview_ta import TA_Handler, Interval
from datetime import datetime
from get_data_from_binance import client
# from get_data_from_binance import my_last_trades

def my_last_trades(asset1):
    trades = client.get_my_trades(symbol=asset1)
    print(f"My {asset1} trades:")
    # print(trades)
    for trade in trades[:10]:
        tt = int(trade.get('time')) / 1000
        time_last_trades = datetime.utcfromtimestamp(tt).strftime('%Y-%m-%d %H:%M:%S')
        symbol = trade.get('symbol')
        price = float(trade.get('price'))
        qty = float(trade.get('qty'))
        quote_qty = float(trade.get('quoteQty'))
        commission = float(trade.get('commission'))
        commission_asset = trade.get('commissionAsset')
        # print(f"time_last_trades: {time_last_trades}, symbol: {symbol}, price: {price},"
        #       f"qty: {qty}, quote_qty {quote_qty}, commis: {commission}, "
        #       f"commisAsset: {commission_asset}")
        exists = db.session.query(myTrades.id).filter_by(symbol=symbol).first() is not None
        if not exists:
            admin2 = myTrades(symbol=symbol, time_last_trades=time_last_trades, , price, qty, quote_qty, commission, commission_asset)
            db.session.add(admin2)
            db.session.commit()
        else:
            admin = AllTickers.query.filter_by(ticker=symbol).first()
            admin.ticker = symbol
            admin.recommendatsion = recommendatsion
            admin.recommendatsion_all_day = recommendatsion_all_day
            db.session.add(admin)
            db.session.commit()
        return time_last_trades, symbol, price, qty, quote_qty, commission, commission_asset


def db_updating_time():
    time1 = datetime.now().strftime("%d/%m/%y %H:%M")
    return time1


def trading_view_recommendation(coin, interval):
    tesla = TA_Handler(
        symbol=f"{coin}USDT",
        screener="CRYPTO",
        exchange="BINANCE",
        interval=interval
    )
    recommend = tesla.get_analysis().summary.get('RECOMMENDATION')
    return recommend


def trading_view_recommendation_all(coin, interval):
    tesla = TA_Handler(
        symbol=f"{coin}",
        screener="CRYPTO",
        exchange="BINANCE",
        interval=interval
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
    # all_pairs = AllTickers.query.order_by(AllTickers.recommendatsion_all_day, AllTickers.recommendatsion).filter(
    #     AllTickers.recommendatsion_all_day == 'BUY', AllTickers.recommendatsion_all_day == 'STRONG_BUY').all()
    all_pairs = db.session.query(AllTickers).filter(
        AllTickers.recommendatsion_all_day.in_(['STRONG_BUY', 'BUY'])).order_by(AllTickers.recommendatsion_all_day,
                                                                                AllTickers.recommendatsion).all()
    print("ok")
    return all_pairs


def all_tradable_pairs(client):
    # t0 = time()
    global recommendatsion, recommendatsion_all_day
    tickers1 = client.get_orderbook_tickers()
    # AllTickers.query.delete()
    count = 0

    for ticker in tickers1:
        bid_price = float(ticker.get('bidPrice'))
        if bid_price > 0:
            count += 1
            symbol = ticker.get('symbol')
            my_last_trades(symbol)
            try:
                recommendatsion = trading_view_recommendation_all(symbol, Interval.INTERVAL_4_HOURS)
                recommendatsion_all_day = trading_view_recommendation_all(symbol, Interval.INTERVAL_1_DAY)
                # t, symbol2, price, qty, quote_qty, commission, commission_asset = my_last_trades(symbol)
            except:
                pass
            exists = db.session.query(AllTickers.id).filter_by(ticker=symbol).first() is not None
            if not exists:
                admin2 = AllTickers(ticker=symbol, recommendatsion=recommendatsion,
                                    recommendatsion_all_day=recommendatsion_all_day)
                db.session.add(admin2)
                db.session.commit()
            else:
                admin = AllTickers.query.filter_by(ticker=symbol).first()
                admin.ticker = symbol
                admin.recommendatsion = recommendatsion
                admin.recommendatsion_all_day = recommendatsion_all_day
                db.session.add(admin)
                db.session.commit()
                print('11111111')
            print(count, symbol, recommendatsion)
    # tt = time() - t0
    # print(tt)
