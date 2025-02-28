from flask import Blueprint, render_template
from ..dao import get_card_prices_by_id  # Import your DAO function
from ..models import Card
from datetime import datetime

card_history_bp = Blueprint('card_history', __name__)

@card_history_bp.route("/card_history/<uuid:id>")
def card_history(id):
    card = Card.query.filter_by(id=id).first()
    if not card:
        return "Card not found", 404
    
    prices = get_card_prices_by_id(card.id)
    price_data = [{"date": price.price_date.strftime('%Y-%m-%d'), "price": price.price} for price in prices]

    # Separate dates and prices for the graph
    dates = [data["date"] for data in price_data]
    prices = [data["price"] for data in price_data]

    return render_template("card_history.html", card=card, price_data=price_data, dates=dates, prices=prices)
