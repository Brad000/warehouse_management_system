import os
import re
from flask import Flask, render_template, redirect, request, flash, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import LoginForm, RegisterForm
from os import path
import bcrypt
if path.exists("env.py"):
    import env


app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get("MONGO_URI")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Home


@app.route('/')
@app.route('/home')
def home():
    users = mongo.db.users.find()
    return render_template("index.html", users=users)

# Login, Logout & Register


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login handler"""
    if session.get('logged_in'):
        if session['logged_in'] is True:
            return redirect(url_for('home', title="Login"))

    form = LoginForm()

    if form.validate_on_submit():
        # returns all users from database
        users = mongo.db.users
        # attempt to find one that matches what has been entered
        db_user = users.find_one({'name': request.form['username'],
                                  'usertype': request.form['usertype']})

        if db_user:
            # check password using hashing
            # puts username and usertype into session
            if bcrypt.hashpw(request.form['password'].encode('utf-8'),
                             db_user['password']) == db_user['password']:
                session['username'] = request.form['username']
                session['usertype'] = request.form['usertype']
                session['logged_in'] = True
                # successful login redirect to home
                return redirect(url_for('home', title="Login", form=form))
            # must have failed set flash message
            flash('Invalid username/password combination')
    return render_template("login.html", title="Login", form=form)


@app.route('/logout')
def logout():
    # Clears session and redirects to home
    session.clear()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles registration functionality"""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # returns all users
        users = mongo.db.users
        # check to see if username exists
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            # hash the entered password
            hash_pass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            # insert the user to DB
            # puts username and usertype into session
            users.insert_one({'name': request.form['username'],
                              'password': hash_pass,
                              'email': request.form['email'],
                              'usertype': request.form['usertype']})
            session['username'] = request.form['username']
            session['usertype'] = request.form['usertype']
            return redirect(url_for('home'))
        # duplicate username set flash message and reload page
        flash('Sorry, that username is already taken - use another')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


# Stock Cards


@app.route('/manage_stock_cards')
def manage_stock_cards():
    return render_template("managestockcard.html",
                           stock_cards=mongo.db.stock_cards.find())


@app.route('/archive_stock_cards')
def archive_stock_cards():
    return render_template("archivestockcard.html",
                           stock_cards=mongo.db.stock_cards.find())


@app.route('/add_stock_cards')
def add_stock_cards():
    return render_template('addstockcard.html',
                           customer=mongo.db.customer.find())


@app.route('/insert_stock_cards', methods=['POST'])
def insert_stock_cards():
    stock_cards = mongo.db.stock_cards
    stock_cards.insert_one(request.form.to_dict())
    flash("Stock Card Added")
    return redirect(url_for('manage_stock_cards'))


@app.route('/edit_stock_cards/<stock_cards_id>')
def edit_stock_cards(stock_cards_id):
    stock_cards = mongo.db.stock_cards.find_one({"_id": ObjectId
                                                (stock_cards_id)})
    customer = mongo.db.customer.find()
    return render_template('editstockcard.html',
                           stock_cards=stock_cards, customer=customer)


@app.route('/update_stock_cards/<stock_cards_id>', methods=["POST"])
def update_stock_cards(stock_cards_id):
    stock_cards = mongo.db.stock_cards
    stock_cards.update_one({'_id': ObjectId(stock_cards_id)},
                           {
                               '$set': {
                                        'customer': request.form.get('customer'),
                                        'product_code': request.form.get('product_code'),
                                        'product_desc': request.form.get('product_desc'),
                                        'unit_weight': request.form.get('unit_weight'),
                                        'unit_per_pallet': request.form.get('unit_per_pallet'),
                                        'supplier': request.form.get('supplier'),
                                        'packaging': request.form.get('packaging'),
                                        'active': "on"
                                        }
    })
    flash("Stock Card Edit Successful")
    return redirect(url_for('manage_stock_cards'))


@app.route('/search_stock_card')
def search_stock_card():
    """Provides logic for search bar"""
    orig_query = request.args['query']
    results = mongo.db.stock_cards.find({
        '$or': [
            {'product_code': re.compile(orig_query, re.IGNORECASE)},
            {'product_desc': re.compile(orig_query, re.IGNORECASE)},
        ]
    })
    return render_template('stockcardsearch.html', query=orig_query, results=results)


@app.route('/delist_stock_cards/<stock_cards_id>')
def delist_stock_cards(stock_cards_id):
    stock_cards = mongo.db.stock_cards
    stock_cards.update_one({'_id': ObjectId(stock_cards_id)},
                           {
                                "$set": {
                                            "active": "off"
                                        }
                            })
    flash("Stock Card Archived")
    return redirect(url_for('manage_stock_cards'))


@app.route('/relist_stock_cards/<stock_cards_id>')
def relist_stock_cards(stock_cards_id):
    stock_cards = mongo.db.stock_cards
    stock_cards.update_one({'_id': ObjectId(stock_cards_id)},
                           {
                               "$set": {
                                            "active": "on"
                               }
                           })
    flash("Stock Card Re-Listed")
    return redirect(url_for('manage_stock_cards'))


@app.route('/delete_stock_cards/<stock_cards_id>')
def delete_stock_cards(stock_cards_id):
    mongo.db.stock_cards.remove({'_id': ObjectId(stock_cards_id)})
    flash("Stock Card Deleted")
    return redirect(url_for('manage_stock_cards'))

# Stock Control


@app.route('/goods_receipt', methods=['POST'])
def goods_receipt():
    goods_receipt = mongo.db.storage
    goods_receipt.insert_one(request.form.to_dict())
    flash("Delivery Receipted")
    return redirect(url_for('home'))


@app.route('/stock_search')
def stock_search():
    return render_template('stocksearch.html')


@app.route('/stock_search_results')
def stock_search_results():
    """Provides logic for search bar"""
    orig_query = request.args['query']
    stock_cards = mongo.db.stock_cards.find()
    results = mongo.db.storage.find({
        '$or': [
            {'customer': re.compile(orig_query, re.IGNORECASE)},
            {'product_code': re.compile(orig_query, re.IGNORECASE)},
            {'delivery_ref': re.compile(orig_query, re.IGNORECASE)},
        ]
    })
    return render_template('stocksearch.html',
                           query=orig_query, results=results, stock_cards=stock_cards)


@app.route('/edit_stock/<storage_id>')
def edit_stock(storage_id):
    product = mongo.db.stock_cards.find()
    stock = mongo.db.storage.find_one({"_id": ObjectId
                                      (storage_id)})
    customer = mongo.db.customer.find()
    return render_template('editstock.html', customer=customer, storage=stock,
                           product=product)


@app.route('/update_stock/<storage_id>', methods=["POST"])
def update_stock(storage_id):
    stock = mongo.db.storage
    stock.update_one({'_id': ObjectId(storage_id)},
                     {
                        '$set': {
                                    'customer': request.form.get('customer'),
                                    'product_code': request.form.get('product_code'),
                                    'delivery_ref': request.form.get('delivery_ref'),
                                    'bbe': request.form.get('bbe'),
                                    'quantity': request.form.get('quantity'),
                                    'location': request.form.get('location'),
                                    'date_received': request.form.get('date_received')
                                }
    })
    flash("Stock Receipt Edit Successful")
    return redirect(url_for('stock_search'))


@app.route('/relocation/<storage_id>')
def relocation(storage_id):
    product = mongo.db.stock_cards.find()
    stock = mongo.db.storage.find_one({"_id": ObjectId
                                      (storage_id)})
    customer = mongo.db.customer.find()
    return render_template('relocatestock.html', customer=customer, storage=stock,
                           product=product)


@app.route('/relocate_stock/<storage_id>', methods=["POST"])
def relocate_stock(storage_id):
    stock = mongo.db.storage
    stock.update_one({'_id': ObjectId(storage_id)},
                     {
                        '$set': {
                                    'location': request.form.get('location'),
                                }
    })
    flash("Stock Relocated")
    return redirect(url_for('stock_search'))


@app.route('/dispatch_stock/<storage_id>', methods=["POST"])
def dispatch_stock(storage_id):
    stock = mongo.db.storage
    stock.update_one({'_id': ObjectId(storage_id)},
                     {
                       "$set": {
                                  "date_dispatched": request.form.get('date_dispatched'),
                                  "in_stock": "off"
                                }
                            })
    flash("Stock Dispatched")
    return redirect(url_for('stock_search'))


@app.route('/dispatch/<storage_id>')
def dispatch(storage_id):
    product = mongo.db.stock_cards.find()
    stock = mongo.db.storage.find_one({"_id": ObjectId
                                      (storage_id)})
    customer = mongo.db.customer.find()
    return render_template('dispatch.html', customer=customer, storage=stock,
                           product=product)


@app.route('/stock_archive')
def stock_archive():
    return render_template("stockarchive.html")


@app.route('/archive_search_results')
def archive_search_results():
    """Provides logic for search bar"""
    orig_query = request.args['query']
    stock_cards = mongo.db.stock_cards.find()
    results = mongo.db.storage.find({
        '$or': [
            {'product_code': re.compile(orig_query, re.IGNORECASE)},
        ]
    })
    return render_template('stockarchive.html',
                           query=orig_query, results=results, stock_cards=stock_cards)


@app.route('/delete_stock/<storage_id>')
def delete_stock(storage_id):
    mongo.db.storage.remove({'_id': ObjectId(storage_id)})
    flash("Stock Deleted")
    return redirect(url_for('stock_search'))


@app.route('/goods_received')
def goods_received():
    customer = mongo.db.customer.find()
    product = mongo.db.stock_cards.find()
    return render_template("goodsreceived.html", customer=customer, product=product)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
