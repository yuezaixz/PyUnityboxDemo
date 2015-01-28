# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import requests
import json

# configuration
DATABASE = '/tmp/demo.db'
DEBUG = True
#warning
API_USERNAME = 'e33a57ff3af940ad'
API_PASSWORD = 'cde662ed9c9a4998'
API_CLIENT_ID = '7895193cda252a8070dd'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def init_app_token():
    if ('ACCESS_TOKEN' in app.config) and app.config['ACCESS_TOKEN']:
        return
    params = {'client_id': app.config['API_CLIENT_ID'],\
              'grant_type': 'password',\
              'password':app.config['API_PASSWORD'],\
              'username':app.config['API_USERNAME']
              }

    r = requests.post("https://api.unity-box.com/oauth2/access_token",\
                      data=params,verify=False)
    if r.status_code == 200:
        responseDict =  r.json()
        app.config['ACCESS_TOKEN'] = responseDict['access_token']
        app.config['TOKEN_TYPE'] = responseDict['token_type']
        app.config['EXPIRES'] = responseDict['expires_in']
        app.config['TOKEN_SCOPE'] = responseDict['scope']
        
@app.before_request
def before_request():
    init_app_token()
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
# @app.route('/')
# def index():
#     return render_template('index.html')
#         
# @app.route('/iframe')
# def iframe():
#     return render_template('iframe.html')

# order about
@app.route('/')
def index():
    return redirect(url_for('show_orders'))

@app.route('/orders/add',methods=['GET'])
def add_order_page():
    return render_template('order_add.html')

@app.route('/orders',methods=['GET'])
def show_orders():
    cur = g.db.execute('select product_name, consignee_name,serial_number from orders order by id desc')
    orders = [dict(product_name=row[0], consignee_name=row[1],serial_number=row[2]) for row in cur.fetchall()]
    return render_template('orders.html', orders=orders)
@app.route('/orders', methods=['POST'])
def add_order():
    product_name = request.form['product_name']
    consignee_name = request.form['consignee_name']
    otp_phone_number = request.form['otp_phone_number']
    consignee_email = request.form['consignee_email']
    pickuppoint = request.form['pickuppoint']
    extra_code = request.form['extra_code']
    remark = request.form['remark']
    order_dict = {'product_name':product_name,'consignee_name':consignee_name,'otp_phone_number':otp_phone_number,'consignee_email':consignee_email,'pickuppoint':pickuppoint}
    headers = {'content-type': 'application/json','Authorization':'%s %s' % (app.config['TOKEN_TYPE'],app.config['ACCESS_TOKEN'])}
    r = requests.post('https://api.unity-box.com/services/order/', data=json.dumps(order_dict), headers=headers,verify=False)
    g.db.execute('insert into orders (product_name, consignee_name, otp_phone_number, consignee_email, pickuppoint, extra_code, remark, serial_number) values (?, ?, ?, ?, ?, ?, ?, ?)',
                 [product_name,consignee_name,otp_phone_number,consignee_email,pickuppoint,extra_code,remark,r.json()['serial_number']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_orders'))
if __name__ == '__main__':
    app.run()
