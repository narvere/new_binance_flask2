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
all_tickers = Table(
    'all_tickers', meta,
    Column('id', Integer, primary_key=True),
    Column('ticker', String(20), nullable=False),
)

usdt_tickers = Table(
    'usdt_tickers', meta,
    Column('id', Integer, primary_key=True),
    Column('ticker', String(20), nullable=False, unique=True),
)

arr = []


async def main():
    client = await AsyncClient.create(api_key, api_secret)
    account = await client.get_account()
    print(account)

    # 1 await all_tradable_pairs(client)
    # await select_from_db()

    # 2 await one_ticker_info(client)

    # await all_usdt_pairs(client)

    await client.close_connection()


async def select_from_db():
    tisks = all_tickers.select().where(all_tickers.c.id > 0)
    result = conn.execute(tisks)
    for row in result:
        t = row[1]
        if t == 'BNBUSDT':
            print(row[1])


async def one_ticker_info(client):
    delete_symbol = usdt_tickers.delete()
    conn.execute(delete_symbol)
    count = 0
    tisks = all_tickers.select().where(all_tickers.c.id > 0)
    result = conn.execute(tisks)
    for symbol1 in result:
        info1 = await client.get_symbol_info(symbol1[1])
        symbol = info1.get('symbol')
        baseAsset = info1.get('baseAsset')
        quoteAsset = info1.get('quoteAsset')
        permissions = info1.get('permissions')
        if 'SPOT' in permissions and quoteAsset == 'USDT':
            print(time(), symbol, baseAsset, quoteAsset, permissions)
            add_symbol = usdt_tickers.insert().values(ticker=symbol)
            # update_symbol = tickers.update().values(ticker=symbol)
            conn.execute(add_symbol)
            await asyncio.sleep(2)


async def all_usdt_pairs(client):
    info = await client.get_exchange_info()
    assets = info.get('symbols')
    counts = 0
    for key3 in assets:
        symbol = key3.get('symbol')
        quoteAsset = key3.get('quoteAsset')
        if quoteAsset == "USDT":
            # print(symbol)
            counts += 1
            return symbol
    # print(counts)


async def all_tradable_pairs(client):
    tickers1 = await client.get_orderbook_tickers()
    delete_symbol = all_tickers.delete()
    conn.execute(delete_symbol)
    count = 0
    for ticker in tickers1:
        bidPrice = float(ticker.get('bidPrice'))
        if bidPrice > 0:
            count += 1
            symbol = ticker.get('symbol')
            add_symbol = all_tickers.insert().values(ticker=symbol)
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
        time = int(trade.get('time')) / 1000
        t = datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        symbol = trade.get('symbol')
        price = trade.get('price')
        qty = trade.get('qty')
        quoteQty = trade.get('quoteQty')
        commission = trade.get('commission')
        commissionAsset = trade.get('commissionAsset')
        print(f"time: {t}, symbol: {symbol}, price: {price},"
              f"qty: {qty}, quoteQty {quoteQty}, commis: {commission}, "
              f"commisAsset: {commissionAsset}")


if __name__ == "__main__":
    t0 = time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    tt = time() - t0
    print(tt)
