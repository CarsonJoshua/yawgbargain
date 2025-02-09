from flask import Blueprint, render_template
from models import Card, CardPrice

card_price_bp = Blueprint('card_price', __name__)

@card_price_bp.route("/card_price/<oracle_id>")
def card_price(oracle_id):
    card = Card.query.filter_by(oracle_id=oracle_id).first()
    if not card:
        return "Card not found", 404
    prices = CardPrice.query.filter_by(oracle_id=card.oracle_id).all()
    price_data = [{"date": price.price_date.strftime('%Y-%m-%d'), "price":price.price} for price in prices]
    return render_template("card_price.html", card=card, price_data=price_data)