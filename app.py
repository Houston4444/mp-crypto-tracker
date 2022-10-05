import json
import os
import sqlite3
import time
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id: int):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    # posts = conn.execute('SELECT * FROM posts').fetchall()
    
    gain = 0.0
    print('stock')
    stocks = conn.execute('SELECT * FROM stock').fetchall()
    moneys = list[dict]()
    now = time.time()
    
    for stock in stocks:
        print(stock['moneyId'], stock['quantity'])
        for mon in moneys_map['data']:
            # print(mon)
            if mon['id'] == stock['moneyId']:
                money = {'full_name': f"({mon['symbol']}) {mon['name']}"}
                moneys.append(money)
    finito = time.time()
    print('temps lle', finito - now)
    conn.close()
    print(moneys)
    
        
    # print('posts::', posts)
    return render_template('index.html', moneys=moneys)

@app.route('/about')
def about():
    print('chien mechant')

@app.route('/<int:post_id>')
def post(post_id: int):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/edit', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        quantity = request.form['quantity']
        money_id = request.form['money']
        print('zlekf', money_id, quantity)
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
                f'SELECT quantity FROM stock WHERE moneyID = {money_id}').fetchone()

            quantity = max(money_stock['quantity'] - quantity, 0.0)
            print('stocking quantity', quantity, money_id)
            conn.execute('UPDATE stock SET quantity = ? WHERE moneyId = ?',
                         (quantity, money_id))
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

    return render_template('create.html', moneys=moneys)

@app.route('/add', methods=('GET', 'POST'))
def edit():
    if request.method == 'POST':
        money = request.form['title']
        quantity = request.form['quantity']
        
        fields_ok = True
        try:
            quantity = float(quantity)
        except:
            flash('Quantité invalide !')
            fields_ok = False

        if not money:
            fields_ok = False
            flash('Une Crypto-Monnaie est requise !')

        conn = get_db_connection()
        
        for mon in moneys_map['data']:
            if mon['name'] == money:
                money_id = mon['id']
                break
        else:
            fields_ok = False
            flash('Crypto-Monnaie "{money}" inconnue !')
            
        if fields_ok:
            money_stock = conn.execute(
                f'SELECT quantity FROM stock WHERE moneyID = {money_id}').fetchone()

            if money_stock is None:
                conn.execute('INSERT INTO stock (moneyId, quantity) VALUES (?, ?)',
                                (money_id, quantity))
            else:
                quantity += money_stock['quantity']
                print('stocking quantity', quantity, money_id)
                conn.execute('UPDATE stock SET quantity = ? WHERE moneyId = ?',
                                (quantity, money_id))

            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template(
        'edit.html',
        moneys=[m['name'] for m in moneys_map['data']])

# @app.route('/edit', methods=('POST',))
# def delete():
#     # post = get_post(id)
#     # conn = get_db_connection()
#     # conn.execute('DELETE FROM posts WHERE id = ?', (id,))
#     # conn.commit()
#     # conn.close()
#     # flash('"{}" was successfully deleted!'.format(post['title']))
#     return redirect(url_for('index'))

this_dir = os.path.dirname(__file__)
with open(os.path.join(this_dir, 'crypto_cur_map.json')) as file:
    moneys_map = json.load(file)
    