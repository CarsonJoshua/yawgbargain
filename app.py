from flask import Flask, render_template, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import date
import pandas as pd
import configparser





# Load configuration from a private config file
config = configparser.ConfigParser()
config.read('config.ini')

# Apply database configuration
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{config["database"]["user"]}:{config["database"]["password"]}@{config["database"]["host"]}/{config['database']['dbname']}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config["database"]["SQLALCHEMY_TRACK_MODIFICATIONS"]

db = SQLAlchemy(app)
from models import Card, CardPrice


@app.route('/')
def index():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    session['user'] = {'name': 'Joshua Carson', 'email': 'joshua@example.com'}
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/decks')
def decks():
    return 'My Decks Page'

@app.route('/profile')
def profile():
    return 'My Profile Page'

@app.route('/pricer', methods=['GET', 'POST'])
def pricer():
    if request.method == 'POST':
        deck_text = request.form.get('deck_list', '').strip()
        if not deck_text:
            # flash("Please enter a deck list.", "error")
            return render_template('pricer.html')

        card_names = [line.strip() for line in deck_text.split("\n") if line.strip()]
        deck_prices = []
        total_price = 0.0

        today = date.today()

        for card_name in card_names:
            card = Card.query.filter_by(name=card_name).first()
            if card:
                latest_price = (
                    CardPrice.query
                    .filter_by(oracle_id=card.oracle_id)
                    .order_by(CardPrice.price_date.desc())  # Get the most recent price
                    .first()
                )
                if latest_price:
                    deck_prices.append((card_name, latest_price.price))
                    total_price += latest_price.price
                else:
                    deck_prices.append((card_name, "Price not found"))
            else:
                deck_prices.append((card_name, "Card not found"))

        return render_template('pricer.html', deck_prices=deck_prices, total_price=total_price)

    return render_template('pricer.html')
@app.route("/card_price/<oracle_id>")
def card_price(oracle_id):
    card = Card.query.filter_by(oracle_id=oracle_id).first()
    if not card:
        return "Card not found", 404
    prices = CardPrice.query.filter_by(oracle_id=card.oracle_id).all()
    price_data = [{"date": price.price_date.strftime('%Y-%m-%d'), "price":price.price} for price in prices]
    return render_template("card_price.html", card=card, price_data=price_data)


if __name__ == '__main__':
    

    app.run(debug=True,host=config["flask"]["host"],port=int(config["flask"]["port"]))

