import os
from flask import Flask, render_template, redirect, request, url_for, request


app = Flask(__name__)


@app.route('/')
@app.route('/manage_stock_cards')
def manage_stock_cards():
    return render_template("stockcard.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
