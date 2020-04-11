import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, request, url_for, config
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)


@app.route('/')
@app.route('/manage_stock_cards')
def manage_stock_cards():
    return render_template("managestockcard.html",
                           stock_cards=mongo.db.stock_cards.find())


@app.route('/add_stock_cards')
def add_stock_cards():
    return render_template('addstockcard.html')


@app.route('/insert_stock_cards', methods=['POST'])
def insert_stock_cards():
    stock_cards = mongo.db.stock_cards
    stock_cards.insert_one(request.form.to_dict())
    return redirect(url_for('manage_stock_cards'))


@app.route('/edit_stock_cards')
def edit_stock_cards():
    return render_template('editstockcard.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
