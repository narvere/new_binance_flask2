from binance_info import status, balances, client, exchange_info
from dbs import db, Assets, PairsInfo
from funcs import trading_view_recommendation, db_updating_time
from tradingview_ta import Interval
from datetime import datetime


def my_last_trades(asset1):
    trades = client.get_my_trades(symbol=asset1)
    print(f"My {asset1} trades:")
    print(trades)
    for trade in trades[:10]:
        tt = int(trade.get('time')) / 1000
        time_last_trades = datetime.utcfromtimestamp(tt).strftime('%Y-%m-%d %H:%M:%S')
        symbol = trade.get('symbol')
        price = float(trade.get('price'))
        qty = float(trade.get('qty'))
        quote_qty = float(trade.get('quoteQty'))
        commission = float(trade.get('commission'))
        commission_asset = trade.get('commissionAsset')
        print(f"time_last_trades: {time_last_trades}, symbol: {symbol}, price: {price},"
              f"qty: {qty}, quote_qty {quote_qty}, commis: {commission}, "
              f"commisAsset: {commission_asset}")
        return time_last_trades, symbol, price, qty, quote_qty, commission, commission_asset


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
