from binance_info import status, balances, client
from dbs import db, Assets


def save_or_update_db():
    exists = db.session.query(Assets.id).filter_by(asset=asset).first() is not None
    if not exists:
        admin = Assets(asset=asset, free=free, locked=locked, total_usd=total_usd, total_eur=total_eur)

        db.session.add(admin)
        db.session.commit()
    else:
        admin = Assets.query.filter_by(asset=asset).first()
        admin.free = free
        admin.locked = locked
        admin.total_usd = total_usd
        admin.total_eur = total_eur

        db.session.add(admin)
        db.session.commit()


def getting_data_from_binance():
    global locked, free, asset, total_usd, total_eur, price_e
    if status.get("msg") == 'normal':
        Assets.query.delete()
        super_total = 0
        for balance in balances:
            locked = float(balance.get("locked"))
            free = float(balance.get("free"))
            if locked > 0 or free > 0:
                asset = str(balance.get("asset"))
                if asset != 'USDT' and asset != 'LDUSDT' and asset != 'BETH':
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
                else:
                    total_usd = round((free + locked), 2)
                super_total += total_usd
                total_usd = round(total_usd, 2)
                # print(asset, free, locked, total_usd, total_eur)
                save_or_update_db()
        # super_total_usd = round(super_total, 2)
        # super_total_eur = round((super_total_usd / price_e), 2)
        # getting_orders()
        # save_or_update_order_db()
        return
    else:
        print("Binance is down")


# def super_super():
#     super_total_usd = round(super_total, 2)
#     super_total_eur = round((super_total_usd / price_e), 2)
#     return super_total_usd, super_total_eur