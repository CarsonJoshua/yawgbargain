from flask import Blueprint, render_template, request
from ..models import Card, CardPrice
from datetime import date

pricer_bp = Blueprint('pricer', __name__)

@pricer_bp.route('/pricer', methods=['GET', 'POST'])
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
