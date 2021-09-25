import pytz
from flask import render_template
from dbs import app

from routes import base, my_coins, all_pairs, get_all_pairs, all_usdt, coin

# pip install flask[async]
# pip install flask
# pip install pytz


zone_ee = pytz.timezone('Europe/Tallinn')

app.add_url_rule('/', 'base', base)

app.add_url_rule('/my_coins/', 'my_coins', my_coins, methods=['POST', 'GET'])

app.add_url_rule('/all_pairs/', 'all_pairs', all_pairs, methods=['POST', 'GET'])

app.add_url_rule('/get_all_pairs/', 'get_all_pairs', get_all_pairs, methods=['POST', 'GET'])

app.add_url_rule('/all_usdt/', 'all_usdt', all_usdt, methods=['POST', 'GET'])

app.add_url_rule('/coin/<coin_name>/', '/coin/<coin_name>/', coin, methods=['POST', 'GET'])


@app.route('/test/')
def test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)
