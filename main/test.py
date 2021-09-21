from dbs import db, Assets, all_tickers

symbol = 'xxx'
free = 111.0
locked = 222.0
total_usd = 333.0
total_eur = 444.0

# exists = db.session.query(all_tickers.id).filter_by(ticker=symbol).first() is not None
# if not exists:
#     admin2 = all_tickers(ticker=symbol)
#     db.session.add(admin2)
#     db.session.commit()
#     print(2)
# else:
#     admin = all_tickers.query.filter_by(ticker=symbol).first()
#     admin.ticker = symbol
#     db.session.add(admin)
#     db.session.commit()
#     print(1)

my_assets = all_tickers.query.order_by(-all_tickers.ticker).all()
for i in my_assets:
    print(i)
# print(my_assets)