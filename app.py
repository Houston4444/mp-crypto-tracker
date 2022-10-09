import json
import os
import sqlite3
import datetime
import logging
import threading
from typing import Optional
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_apscheduler import APScheduler

import coin_api_caller
import graph_maker

# only because API free key is limited.
# will be removed.
CALL_API = True

# for testing, it's easier to check cryto quotes each minute
# than each day.
EACH_MINUTE = False

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(
        'database.db',
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    return conn

def get_evolution_sym_from_int(evolution: Optional[int]) -> str:
    if evolution is None:
        return ''
    if evolution <= -1:
        return "↘"
    if evolution <= 0:
        return "→"
    if evolution <= 1:
        return "↗"
    return "⇗"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
main_config = {'gains_drawn': False}
_logger = logging.Logger(__name__)
_logger.setLevel(logging.INFO)

@app.route('/')
def index():
    conn = get_db_connection()
    
    stocks = conn.execute('SELECT * FROM stock').fetchall()
    moneys = list[dict]()
    
    for stock in stocks:
        for mon in moneys_map['data']:
            if mon['id'] == stock['moneyId']:
                money = {
                    'full_name': f"({mon['symbol']}) {mon['name']}",
                    'symbol': mon['symbol'],
                    'name': mon['name'],
                    'evol_sym': get_evolution_sym_from_int(stock['moneyEvolution'])}
                             
                icon = f"{mon['symbol'].lower()}.png"
                if os.path.exists(os.path.join('static', 'crypto_icons', icon)):
                    money['icon'] = 'crypto_icons/' + icon

                moneys.append(money)
                break

    last_gain = conn.execute(
        'SELECT gain FROM gains ORDER BY day DESC LIMIT 1').fetchone()
    
    if last_gain is None or last_gain['gain'] == 0.0:
        gain_str = '0.00 €'
    elif last_gain['gain'] > 0.0:
        gain_str = "+ %.2f €" % last_gain['gain']
    else:
        gain_str = "- %.2f €" % abs(last_gain['gain'])
    
    conn.close()            
    return render_template('index.html', moneys=moneys, gain=gain_str)

@app.route('/edit', methods=('GET', 'POST'))
def route_edit():
    if request.method == 'POST':
        quantity = request.form['quantity']
        money_id = request.form['money']

        fields_ok = True
        
        try:
            quantity = float(quantity)
        except ValueError:
            fields_ok = False
            flash('Quantité non valide')
        
        if fields_ok and not money_id:
            flash('Une Crypto-Monnaie est requise !')
            fields_ok = False
        
        if fields_ok:
            conn = get_db_connection()
            
            money_stock = conn.execute(
                f'SELECT * FROM stock WHERE moneyID = {money_id}').fetchone()

            if money_stock is None:
                _logger.warning(
                    'attempting to remove some stock user has not'
                    ', that should not happens !!!')

            if not money_stock['quantity'] == 0.0:
                # prevented Zero Division
                # update quantity and total expense for this crypo.
                new_quantity = max(money_stock['quantity'] - quantity, 0.0)
                new_total_expense = (money_stock['totalExpense']
                                     * (quantity / money_stock['quantity']))
                conn.execute(
                    f'UPDATE stock SET quantity={new_quantity}, '
                    f'totalExpense={new_total_expense} WHERE moneyId = {money_id}')

            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    moneys = list[dict[str, str]]()
    conn = get_db_connection()
    money_ids = conn.execute('SELECT moneyId FROM stock').fetchall()
    for moni in money_ids:
        for mon in moneys_map['data']:
            if mon['id'] == moni['moneyId']:
                moneys.append(
                    {'display_name': f"({mon['symbol']}) {mon['name']}",
                     'id': mon['id']})
                break

    return render_template('edit.html', moneys=moneys)

@app.route('/add', methods=('GET', 'POST'))
def route_add():
    if request.method == 'POST':
        fields_ok = True

        try:
            money = request.form['crypto_name']
            quantity = request.form['quantity']
            buy_price = request.form['buy_price']
        except:
            _logger.warning("requête POST sur /add non valide")
            fields_ok = False
        
        if fields_ok:        
            try:
                quantity = float(quantity)
                buy_price = float(buy_price)
            except ValueError:
                flash("Quantité ou prix d'achat invalide !")
                fields_ok = False

            if not money:
                fields_ok = False
                flash('Une Crypto-Monnaie est requise !')

            for mon in moneys_map['data']:
                if mon['name'] == money:
                    money_id = mon['id']
                    break
            else:
                fields_ok = False
                flash('Crypto-Monnaie "{money}" inexistante ou non référencée !')

        if fields_ok:
            conn = get_db_connection()
            money_stock = conn.execute(
                f'SELECT * FROM stock WHERE moneyID = {money_id}').fetchone()

            if money_stock is None:
                # user never bought this crypto before
                # we add a new row to the table 
                conn.execute(
                    'INSERT INTO stock (moneyId, quantity, totalExpense) '
                    'VALUES (?, ?, ?)',
                    (money_id, quantity, buy_price * quantity))
            else:
                # user already bought this crypto before
                # we update quantity and total cost for this crypto
                total_expense = money_stock['totalExpense'] + quantity * buy_price
                quantity += money_stock['quantity']
                conn.execute(
                    f'UPDATE stock SET quantity={quantity}, '
                    f'totalExpense={total_expense} '
                    f'WHERE moneyId = {money_id}')

            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template(
        'add.html',
        moneys=[m['name'] for m in moneys_map['data']],
        autocomplete=True)


@app.route('/gains')
def route_gains():
    if not main_config['gains_drawn']:
        conn = get_db_connection()
        
        gains = conn.execute('SELECT gain FROM gains').fetchall()
        gain_list = [g['gain'] for g in gains]
        if len(gain_list) == 1:
            # make it draw a straight line
            # if we've got only one value.
            gain_list.append(gain_list[0])
        
        conn.close()
        
        _logger.info('making the gain curve')
        graph_maker.make_graph(gain_list)
        main_config['gains_drawn'] = True
    
    return render_template('gains.html')

def check_crypto_values():
    ''' this function is called every day,
        it checks crypto-currencies values. '''
    if not CALL_API:
        return
    
    _logger.info('Check cryptocurrencies values now.')
    
    # we will now calculate the new gain,
    # so if user calls gains graph, it has to be redrawn.
    main_config['gains_drawn'] = False
    
    conn = get_db_connection()
    stocks = conn.execute('SELECT * FROM STOCK').fetchall()
    today_gain = 0.0

    for stock in stocks:
        q = stock['quantity']
        if q == 0.0:
            continue

        new_price = coin_api_caller.get_coin_api_value(stock['moneyId'])
        evolution = 0
        
        # TODO try it !!!
        if not (stock['lastPrice'] is None or stock['moneyEvolution'] is None):
            if new_price > stock['lastPrice']:
                if stock['moneyEvolution'] >= 1:
                    evolution = 2
                else:
                    evolution = 1
                evolution = 2 if stock['moneyEvolution'] >= 1 else 1
                
            else:
                evolution = -1
        
        conn.execute(f'UPDATE stock SET moneyEvolution={evolution}, '
                     f'lastPrice={new_price} '
                     'WHERE moneyId = %i' % stock['moneyId'])   

        today_gain += (new_price - (stock['totalExpense'] / q)) * q

    conn.execute('INSERT INTO gains (day, gain) VALUES (?, ?)',
                 (datetime.datetime.now(), today_gain))
    conn.commit()
    conn.close()

scheduler = APScheduler()

if EACH_MINUTE:
    scheduler.add_job('check_crypto_values',
                      check_crypto_values,
                      trigger='interval',
                      minutes=1)
else:
    scheduler.add_job('check_crypto_values',
                      check_crypto_values,
                      trigger='interval',
                      days=1)
scheduler.init_app(app)
scheduler.start()
    
this_dir = os.path.dirname(__file__)
with open(os.path.join(this_dir, 'crypto_cur_map.json')) as file:
    moneys_map = json.load(file)


if __name__ == '__main__':
    app.run()