import asyncio
from datetime import datetime
from time import time
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
from binance_info import api_key, api_secret

from binance import AsyncClient

meta = MetaData()
#
engine = create_engine('sqlite:///binance2.db')
conn = engine.connect()
#
Binance_tickers = Table(
    'Binance_tickers', meta,
    Column('id', Integer, primary_key=True),
    Column('ticker', String(20), nullable=False),
)

Usdt_tickers = Table(
    'Usdt_tickers', meta,
    Column('id', Integer, primary_key=True),
    Column('ticker', String(20), nullable=False, unique=True),
)
# Если надо загрузить данные с сервера снимаю коммент и отключаю main()
# meta.create_all(engine)

arr = []


async def mains():
    client = await AsyncClient.create(api_key, api_secret)
    # account = await client.get_account()
    # print(account)

    await all_tradable_pairs(client)
    # await select_from_db()

    # 2await one_ticker_info(client)

    # await all_usdt_pairs(client)

    await client.close_connection()


async def select_from_db():
    tisks = Binance_tickers.select().where(Binance_tickers.c.id > 0)
    result = conn.execute(tisks)
    for row in result:
        t = row[1]
        if t == 'BNBUSDT':
            print(row[1])


async def one_ticker_info(client):
    print(111)
    # delete_symbol = Binance_tickers.delete()
    # conn.execute(delete_symbol)
    tisks = Binance_tickers.select().where(Binance_tickers.c.id > 0)
    result = conn.execute(tisks)
    for symbol1 in result:
        info1 = await client.get_symbol_info(symbol1[1])
        symbol = info1.get('symbol')
        base_asset = info1.get('base_asset')
        quote_asset = info1.get('quote_asset')
        permissions = info1.get('permissions')
        if 'SPOT' in permissions and quote_asset == 'USDT':
            print(time(), symbol, base_asset, quote_asset, permissions)
            add_symbol = Binance_tickers.insert().values(ticker=symbol)
            # update_symbol = tickers.update().values(ticker=symbol)
            conn.execute(add_symbol)
            await asyncio.sleep(2)


async def all_usdt_pairs(client):
    info = await client.get_exchange_info()
    assets = info.get('symbols')
    counts = 0
    for key3 in assets:
        symbol = key3.get('symbol')
        quote_asset = key3.get('quote_asset')
        if quote_asset == "USDT":
            # print(symbol)
            counts += 1
            return symbol
    # print(counts)


async def all_tradable_pairs(client):
    tickers1 = await client.get_orderbook_tickers()
    # delete_symbol = all_tickers.delete()
    # conn.execute(delete_symbol)
    count = 0
    for ticker in tickers1:
        bid_price = float(ticker.get('bid_price'))
        if bid_price > 0:
            count += 1
            symbol = ticker.get('symbol')
            add_symbol = Binance_tickers.insert().values(ticker=symbol)
            # update_symbol = tickers.update().values(ticker=symbol)
            conn.execute(add_symbol)
            print(count, symbol)

            # arr.append(symbol)
    # print(arr)


async def my_assets(account, client):
    count = 0
    for key, value in account.items():
        if key == 'balances':
            for val in value[:2]:
                asset = val.get('asset')
                free = float(val.get('free'))
                locked = float(val.get('locked'))
                try:
                    currencies = ['USDT']
                    for cur in currencies:
                        if free > 0 or locked > 0:
                            count += 1
                            for key1, value2 in val.items():
                                print(key1, value2)
                            total = free + locked
                            print('---------')
                            print("total: {:.8f}".format(total))
                            await my_last_trades(asset, client, cur)
                            print("****")
                            print(count)
                except:
                    pass


async def my_last_trades(asset, client, cur):
    trades = await client.get_my_trades(symbol=asset + cur)
    print(f"My {asset} trades:")
    for trade in trades[:3]:
        time_last_trades = int(trade.get('time')) / 1000
        t = datetime.utcfromtimestamp(time_last_trades).strftime('%Y-%m-%d %H:%M:%S')
        symbol = trade.get('symbol')
        price = trade.get('price')
        qty = trade.get('qty')
        quote_qty = trade.get('quote_qty')
        commission = trade.get('commission')
        commission_asset = trade.get('commission_asset')
        print(f"time_last_trades: {t}, symbol: {symbol}, price: {price},"
              f"qty: {qty}, quote_qty {quote_qty}, commis: {commission}, "
              f"commisAsset: {commission_asset}")


if __name__ == "__main__":
    t0 = time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mains())
    tt = time() - t0
    print(tt)


