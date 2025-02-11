from flask import Blueprint, render_template, request
from ..models import Card, CardPrice
from ..extensions import db
from sqlalchemy import func
from sqlalchemy.orm import aliased
from datetime import date
import decimal

pricer_bp = Blueprint('pricer', __name__)

@pricer_bp.route('/pricer', methods=['GET', 'POST'])
def pricer():
    if request.method == 'POST':
        deck_text = request.form.get('deck_list', '').strip()
        if not deck_text:
            # flash("Please enter a deck list.", "error")
            return render_template('pricer.html')

        card_names = [line.strip() for line in deck_text.split("\n") if line.strip()]

        latest_prices = aliased(CardPrice)

        lowest_prices = (
            db.session.query(
                Card.name,
                func.min(latest_prices.price)  # Get the lowest price
            )
            .join(latest_prices, Card.id == latest_prices.card_id)
            .group_by(Card.name, latest_prices.price_date)  # Group by name and date
            .order_by(latest_prices.price_date.desc())  # Sort by latest price_date
            .all()
        )

        deck_prices = [(name, price if price is not None else "Price not found") for name, price in lowest_prices]
        total_price = sum(price for _, price in deck_prices if isinstance(price, (int, float)))


        return render_template('pricer.html', deck_prices=deck_prices, total_price=total_price)

    return render_template('pricer.html')
