from dbs import AllTickers, myTrades, db, Assets, PairsInfo
from time import time
from tradingview_ta import TA_Handler, Interval
# from datetime import datetime
# from get_data_from_binance import client
from binance_info import status, balances, client, exchange_info
# from funcs import trading_view_recommendation, db_updating_time
from datetime import datetime


# def my_last_trades(asset1):
#     trades = client.get_my_trades(symbol=asset1)
#     print(f"My {asset1} trades:")
#     print(trades)
#     for trade in trades[:10]:
#         tt = int(trade.get('time')) / 1000
#         time_last_trades = datetime.utcfromtimestamp(tt).strftime('%Y-%m-%d %H:%M:%S')
#         symbol = trade.get('symbol')
#         price = float(trade.get('price'))
#         qty = float(trade.get('qty'))
#         quote_qty = float(trade.get('quoteQty'))
#         commission = float(trade.get('commission'))
#         commission_asset = trade.get('commissionAsset')
#         print(f"time_last_trades: {time_last_trades}, symbol: {symbol}, price: {price},"
#               f"qty: {qty}, quote_qty {quote_qty}, commis: {commission}, "
#               f"commisAsset: {commission_asset}")
#         return time_last_trades, symbol, price, qty, quote_qty, commission, commission_asset


def a_price(symbol):
    avg_price = client.get_avg_price(symbol=symbol)
    price = avg_price.get('price')
    return price


def pairs_info_from_binance():
    for item in exchange_info.get('symbols'):
        symbol = str(item.get("symbol"))
        baseAsset = str(item.get("baseAsset"))
        quoteAsset = str(item.get("quoteAsset"))
        orderTypes = str(item.get("orderTypes"))
        permissions = str(item.get("permissions"))
        price = a_price(symbol)
        print(symbol, price)
        exists = db.session.query(PairsInfo.id).filter_by(symbol=symbol).first() is not None
        if not exists:
            pairs_info = PairsInfo(symbol=symbol, baseAsset=baseAsset, quoteAsset=quoteAsset, orderTypes=orderTypes,
                                   permissions=permissions, test=price)
            db.session.add(pairs_info)
            db.session.commit()
        else:
            admin = PairsInfo.query.filter_by(symbol=symbol).first()
            admin.baseAsset = baseAsset
            admin.quoteAsset = quoteAsset
            admin.orderTypes = orderTypes
            admin.permissions = permissions
            admin.test = price
            db.session.add(admin)
            db.session.commit()


def save_or_update_db():
    exists = db.session.query(Assets.id).filter_by(asset=asset).first() is not None
    if not exists:
        # добавление данных в пустую таблицу
        admin = Assets(asset=asset, free=free, locked=locked, total_usd=total_usd, total_eur=total_eur,
                       recommendatsion=recommendatsion, recommendatsion_d1=recommendatsion_d1, price=price)
        db.session.add(admin)
        db.session.commit()

    else:
        # обновление данных
        admin = Assets.query.filter_by(asset=asset).first()
        admin.free = free
        admin.locked = locked
        admin.total_usd = total_usd
        admin.total_eur = total_eur
        admin.recommendatsion = recommendatsion
        admin.price = price

        db.session.add(admin)
        db.session.commit()


def get_prices(symbol):
    avg_price = client.get_avg_price(symbol=symbol)
    price = avg_price.get('price')
    print(price)


def getting_data_from_binance():
    global locked, free, asset, total_usd, total_eur, price_e, recommendatsion, recommendatsion_d1, price
    if status.get("msg") == 'normal':
        super_total = 0
        for balance in balances:
            locked = float(balance.get("locked"))
            free = float(balance.get("free"))
            if locked > 0 or free > 0:
                asset = str(balance.get("asset"))
                if asset != 'USDT' and asset != 'BETH':
                    try:
                        print(asset)
                        recommendatsion = trading_view_recommendation(asset, Interval.INTERVAL_4_HOURS)
                        recommendatsion_d1 = trading_view_recommendation(asset, Interval.INTERVAL_1_DAY)

                        avg_price_usd = client.get_avg_price(symbol=f'{asset}USDT')
                        price_eur = client.get_avg_price(symbol=f'EURUSDT')
                        price_e = round(float(price_eur.get("price")), 5)
                        price = round(float(avg_price_usd.get("price")), 5)
                        # price = 1
                        # print(f"1 {asset} = {price} USDT, EUR = {price_eur}")
                        free = float(balance.get("free"))
                        locked = float(balance.get("locked"))
                        total_usd = round((free + locked) * price, 2)
                        total_eur = round(total_usd / float(price_e), 2)
                    except:
                        recommendatsion = "No info"
                        recommendatsion_d1 = "No info"
                        print(asset)

                else:
                    total_usd = round((free + locked), 2)
                super_total += total_usd
                total_usd = round(total_usd, 2)
                # print(asset, free, locked, total_usd, total_eur)
                save_or_update_db()
        time_1 = db_updating_time()
        return time_1
    else:
        print("Binance is down")


# def super_super():
#     super_total_usd = round(super_total, 2)
#     super_total_eur = round((super_total_usd / price_e), 2)
#     return super_total_usd, super_total_eur


def my_last_trades(asset1):
    trades = client.get_my_trades(symbol=asset1)
    print(f"My {asset1} trades:")
    print(trades)
    for trade in trades[:10]:
        tt = int(trade.get('time')) / 1000
        time_last_trades = datetime.utcfromtimestamp(tt).strftime('%Y-%m-%d %H:%M:%S')
        binance_id = trade.get('id')
        orderId = trade.get('orderId')
        symbol = trade.get('symbol')
        price = float(trade.get('price'))
        qty = float(trade.get('qty'))
        quote_qty = float(trade.get('quoteQty'))
        commission = float(trade.get('commission'))
        commission_asset = trade.get('commissionAsset')
        print(f"time_last_trades: {time_last_trades}, symbol: {symbol}, price: {price},"
              f"qty: {qty}, quote_qty {quote_qty}, commis: {commission}, "
              f"commisAsset: {commission_asset}")
        exists = db.session.query(myTrades.id).filter_by(binance_id=binance_id).first() is not None
        if not exists:
            admin = myTrades(symbol=symbol, time_last_trades=time_last_trades, price=price, qty=qty,
                             quote_qty=quote_qty, commis=commission, commisAsset=commission_asset,
                             binance_id=binance_id, orderId=orderId)
            db.session.add(admin)
        db.session.commit()
    #     else:
    #         admin = myTrades.query.filter_by(symbol=symbol).first()
    #         admin.symbol = symbol
    #         admin.time_last_trades = time_last_trades
    #         admin.binance_id = binance_id
    #         admin.orderId = orderId
    #         admin.price = price
    #         admin.qty = qty
    #         admin.quote_qty = quote_qty
    #         admin.commis = commission
    #         admin.commisAsset = commission_asset
    #         db.session.add(admin)
    #     db.session.commit()
    #     print("commited")
    #     return time_last_trades, symbol, price, qty, quote_qty, commission, commission_asset, binance_id, orderId


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
    # global recommendatsion, recommendatsion_all_day
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
            except:
                pass

    # tt = time() - t0
    # print(tt)
