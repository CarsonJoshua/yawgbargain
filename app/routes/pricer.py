from flask import Blueprint, render_template, request
from ..models import Card, CardPrice
from ..extensions import db
from sqlalchemy import func
from sqlalchemy.orm import aliased

pricer_bp = Blueprint('pricer', __name__)

@pricer_bp.route('/pricer', methods=['GET', 'POST'])
def pricer():
    if request.method == 'POST':
        deck_list = request.form.get('deck_list', '').strip()
        if not deck_list:
            return render_template('pricer.html')

        card_entries = []
        for line in deck_list.split("\n"):
            line = line.strip()
            if line:
                match = re.match(r'(\d+)\s+(.*)', line)
                if match:
                    amount = int(match.group(1))
                    card_name = match.group(2)
                else:
                    amount = 1
                    card_name = line
                card_entries.append((amount, card_name))

        latest_price_subquery = (
            db.session.query(
                CardPrice.card_id,
                func.max(CardPrice.price_date).label('latest_price_date')  
            )
            .group_by(CardPrice.card_id) 
            .join(Card, CardPrice.card_id == Card.id) 
            .filter(Card.name.in_(name for _, name in card_entries))  
            .subquery()
        )

        lowest_prices = (
            db.session.query(
                Card.name,
                func.min(CardPrice.price).label('lowest_price')  
            )
            .join(Card, CardPrice.card_id == Card.id) 
            .join(latest_price_subquery, 
                (CardPrice.card_id == latest_price_subquery.c.card_id) &
                (CardPrice.price_date == latest_price_subquery.c.latest_price_date) 
            )
            .group_by(Card.name)  
            .all()
        )

        deck_prices = [
            (amount, name, price if price is not None else "Price not found") 
            for (amount, name), (name, price) in zip(card_entries, lowest_prices)
        ] + [
            (amount, name, "Card not found") 
            for amount, name in card_entries
            if name not in {val[0] for val in lowest_prices}
        ]
        total_price = sum(price for _,_, price in lowest_prices)


        return render_template('pricer.html', deck_list=deck_list, deck_prices=deck_prices, total_price=total_price)

    return render_template('pricer.html')
