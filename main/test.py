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

# from dbs import myTrades, db, app
# with app.app_context():
# #     db.session.query(myTrades).delete()
# #     db.session.commit()
#
#     pair = ['BTCUSDT']
#     all_pairs_info = db.session.query(myTrades).filter(
#             myTrades.symbol.in_([pair])).order_by(myTrades.symbol).all()
#
#     print(all_pairs_info)

# class Base:
#     "Основной класс"
#     x = 1
#     y = 1
#     # def __init__(self, times, times_a, times_all, my_assets, number, super_total_eur, super_total_usd):
#     self.times = times
#     self.times_a = times_a
#     self.times_all = times_all
#     self.my_assets = my_assets
#     self.number = number
#     self.super_total_eur = super_total_eur
#     self.super_total_usd = super_total_usd

# ph = Base()
# ph.x = 5
# ph.y = 10
# print(ph.x, ph.y)


# print(Base.__doc__)
# print(Base.__name__)
# print(ph.__dict__)
# print(dir(Base))

# getattr(obj, name[,default]) - возвращает значение атрибута объекта
# hasattr(obj, name) - проверяет на наличие атрибута name в obj
# setattr(obj, name, value) - задает значение атрибута
# delattr(obj, name) - удаляет атрибут с именем name

# print(getattr(ph, 'x'))
# print(getattr(ph, 'z', False))
# print(hasattr(ph, 'y'))
# setattr(ph, 'g', 7)
# print(ph.__dict__)
# delattr(ph, 'g')
# print(ph.__dict__)
# setattr(Base, 'g', 7)
# print(Base.__dict__)
#
# Base.xxx = 1000
# ph.yyy  = 5
# print(isinstance(ph, Base))

# class Point:
#     def __init__(self, x=0, y=0):
#         print("Создание экземпляра класса Point")
#         self.x = x
#         self.y = y
#     x = 1
#     y = 1
#     def __del__(self):
#         print("Удаление экземпляра класса Point " +self.__str__())
#
#     def setCoords(self, x, y):
#         self.a = x
#         self.b = y
#
#
# pt = Point()
# pt2 = Point(5)
# pt3 = Point(5,10)
#
# # pt.setCoords(5, 6)
# print(pt.__dict__)
# print(pt2.__dict__)
# print(pt3.__dict__)
# # Point.setCoords(pt, 5, 10)
# # print(pt.__dict__)
# # print(pt.x)


# tp.x = int(input("Введите X: "))
# tp.y = int(input("Введите Y: "))
# tp.z = int(input("Введите Z: "))
# print(tp.__dict__)

class Human:
    def __init__(self, gender, population):
        self.gender = gender
        self.population = population

man = Human(gender=1, population=1)

man.gender = 'Male'
man.population = 15000

print(man.__dict__)