from flask import Blueprint, render_template
from ..models import Card, CardPrice

card_price_bp = Blueprint('card_price', __name__)

@card_price_bp.route("/card_price/<id>")
def card_price(id):
    card = Card.query.filter_by(id=id).first()
    if not card:
        return "Card not found", 404
    prices = CardPrice.query.filter_by(card_id=card.id).all()
    price_data = [{"date": price.price_date.strftime('%Y-%m-%d'), "price":price.price} for price in prices]
    return render_template("card_price.html", card=card, price_data=price_data)