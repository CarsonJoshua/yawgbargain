from flask import Blueprint, render_template, request
from ..models import Card, CardPrice
from ..extensions import db
from sqlalchemy import func
from sqlalchemy.orm import aliased

pricer_bp = Blueprint('pricer', __name__)

@pricer_bp.route('/pricer', methods=['GET', 'POST'])
def pricer():
    if request.method == 'POST':
        deck_text = request.form.get('deck_list', '').strip()
        if not deck_text:
            # flash("Please enter a deck list.", "error")
            return render_template('pricer.html')

        card_names = [line.strip() for line in deck_text.split("\n") if line.strip()]


        # lowest_prices = (
        #     db.session.query(
        #         db.session.query(
        #             CardPrice.card_id,
        #             func.max(CardPrice.price_date)
        #         )
        #         .group_by(CardPrice.card_id)
        #         .join(
        #             Card,
        #             CardPrice.card_id == Card.id
        #         )
        #         .filter(Card.name.in_(card_names))
        #         .subquery(),
        #         func.min(CardPrice.price)
        #     )
        #     .group_by(Card.name)
        #     .all()
        # )

        
        latest_price_subquery = (
            db.session.query(
                CardPrice.card_id,
                func.max(CardPrice.price_date).label('latest_price_date')  
            )
            .group_by(CardPrice.card_id) 
            .join(Card, CardPrice.card_id == Card.id) 
            .filter(Card.name.in_(card_names))  
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

        deck_prices = [(name, price if price is not None else "Price not found") for name, price in lowest_prices] + [(name, "Card not found") for name in set(card_names) - set([val[0] for val in lowest_prices])]
        total_price = sum(price for _, price in deck_prices)


        return render_template('pricer.html', deck_prices=deck_prices, total_price=total_price)

    return render_template('pricer.html')
