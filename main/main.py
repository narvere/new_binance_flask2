import pytz
from flask import render_template
from dbs import app, db, AllTickers
from flask.views import View

from routes import base, my_coins, all_pairs, get_all_pairs, all_usdt, coin, login, info_tickers

# pip install flask[async]
# pip install flask
# pip install pytz
# pip install flask-script
# pip install flask-wtf
# pip install Flask-Views
# pip install python-dotenv

# >>> from main2 import app
# >>> app.url_map

# https://pythonru.com/uroki/11-rabota-s-formami-vo-flask

zone_ee = pytz.timezone('Europe/Tallinn')

app.add_url_rule('/', 'base', base)

app.add_url_rule('/my_coins/', 'my_coins', my_coins, methods=['POST', 'GET'])

app.add_url_rule('/get_all_pairs/', 'get_all_pairs', get_all_pairs, methods=['POST', 'GET'])

app.add_url_rule('/all_pairs/', 'all_pairs', all_pairs, methods=['POST', 'GET'])

app.add_url_rule('/all_usdt/', 'all_usdt', all_usdt, methods=['POST', 'GET'])

app.add_url_rule('/coin/<coin_name>/', '/coin/<coin_name>/', coin, methods=['POST', 'GET'])

app.add_url_rule('/login/', 'login', login, methods=['POST', 'GET'])

app.add_url_rule('/info_tickers/', 'info_tickers', info_tickers, methods=['POST', 'GET'])


@app.route('/test/')
def test():
    all_pairs1 = db.session.query(AllTickers).filter(
        AllTickers.recommendatsion_all_day.in_(['STRONG_BUY', 'BUY'])).order_by(AllTickers.recommendatsion_all_day,
                                                                                AllTickers.recommendatsion).all()
    return render_template('test.html', all_pairs=all_pairs1)


if __name__ == '__main__':
    app.run(debug=True)
