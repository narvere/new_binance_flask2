from tradingview_ta import TA_Handler, Interval

# tesla = TA_Handler(
#     symbol="ATOMUSDT",
#     screener="CRYPTO",
#     exchange="BINANCE",
#     interval=Interval.INTERVAL_1_DAY
# )
# # recommend = tesla.get_analysis().summary.get('RECOMMENDATION')
# recommend = tesla.get_analysis().summary
# print(recommend)


# ###############
# from funcs import trading_view_recommendation
# import sqlite3
#
# conn = sqlite3.connect('binance.db')
# cursor = conn.execute("SELECT * FROM assets")
# rows = cursor.fetchall()
#
#
# def remonendacion():
#     for row in rows:
#         try:
#             recomm = trading_view_recommendation(row[1])
#             coin = row[1]
#             return coin, recomm
#         except Exception as e:
#             print(f"{row[1]} is not found")


###############
# my_assets = Assets.query.order_by(-Assets.total_usd).all()
# result = [r for r, in my_assets]
# print(result)
# from dbs import Assets, db


# def count_of_coins(xxx):
#     numbers = db.session.query(db.func.count(xxx.id)).filter(recommendatsion='BUY')
#     .query.filter_by(username='peter').first()
#     print(numbers)
#
#     qry = (db.session.query(db.func.count(xxx.id))
#            .filter(xxx.recommendatsion.like("BUY")))
#
#     qry = select([func.count(xxx.id)],
#                  and_(xxx.company == 31,
#                       xxx.date.like('2010-05%')
#                       ))


#     peter = xxx.query.filter_by.count(recommendatsion='BUY')
#     print(qry)
#
#     for nr in numbers:
#         for number in nr:
#             print(number)
#             return number
# count_of_coins(Assets)
# from binance_info import client
#
# avg_price = client.get_avg_price(symbol='BTCUSDT')
# price = avg_price.get('price')
# print(price)


# orders = client.get_open_orders()
# for item in orders:
#     symbol = item.get("symbol")
#     price = item.get("price")
#     origQty = item.get("origQty")
#     side = item.get("side")
#     order_type = item.get("type")
#     stopPrice = item.get("stopPrice")
#     time = item.get("time")
#     print(symbol)


# tickers1 = client.get_orderbook_tickers()
# for item in tickers1[:3]:
#     print(item)


# info = client.get_exchange_info()
# for item in info.get('symbols'):
#     symbol = item.get("symbol")
#     baseAsset = item.get("baseAsset")
#     quoteAsset = item.get("quoteAsset")
#     orderTypes = item.get("orderTypes")
#     permissions = item.get("permissions")

# from dbs import PairsInfo, Assets, db, AllTickers, app
# with app.app_context():
#     all_pairs = db.session.query(PairsInfo).filter(
#             PairsInfo.baseAsset.in_(['AAVE'])).order_by(PairsInfo.symbol).all()
#     print(all_pairs)


from funcs import my_last_trades
import asyncio

# from binance_info import client
# def mail():
#     trades = client.get_my_trades(symbol="BTCUSDT")
#     for trade in trades[:10]:
#         print(trade)
#
# mail()

from dbs import myTrades, db, app
with app.app_context():
#     db.session.query(myTrades).delete()
#     db.session.commit()

    pair = ['BTCUSDT']
    all_pairs_info = db.session.query(myTrades).filter(
            myTrades.symbol.in_([pair])).order_by(myTrades.symbol).all()

    print(all_pairs_info)