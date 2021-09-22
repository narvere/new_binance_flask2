# from tradingview_ta import TA_Handler, Interval, Exchange
#
# tesla = TA_Handler(
#     symbol="CELRUSDT",
#     screener="CRYPTO",
#     exchange="BINANCE",
#     interval=Interval.INTERVAL_4_HOURS
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
from dbs import Assets, db


def count_of_coins(xxx):
    # numbers = db.session.query(db.func.count(xxx.id)).filter(recommendatsion='BUY')
    # .query.filter_by(username='peter').first()
    # print(numbers)

    # qry = (db.session.query(db.func.count(xxx.id))
    #        .filter(xxx.recommendatsion.like("BUY")))

    qry = select([func.count(xxx.id)],
                 and_(xxx.company == 31,
                      xxx.date.like('2010-05%')
                      ))


    # peter = xxx.query.filter_by.count(recommendatsion='BUY')
    print(qry)

    # for nr in numbers:
    #     for number in nr:
    #         print(number)
    #         return number
count_of_coins(Assets)