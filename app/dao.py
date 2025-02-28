
from sqlalchemy import func, any_, or_
from .models import db, Card, CardPrice



def get_latest_prices(card_names, price_date):
    if not card_names:
        return {}

    latest_price_subquery = (
        db.session.query(
            CardPrice.card_id,
            func.max(CardPrice.price_date).label('latest_price_date')
        )
        .filter(CardPrice.price_date <= price_date)
        .group_by(CardPrice.card_id)
        .join(Card, CardPrice.card_id == Card.id)
        .subquery()
    )

    lowest_prices = (
        db.session.query(
            Card.name,
            Card.id,
            func.min(CardPrice.price).label('lowest_price')
        )
        .filter(func.lower(Card.name).in_([name.lower() for name in card_names]))
        .join(latest_price_subquery,
            (CardPrice.card_id == latest_price_subquery.c.card_id) &
            (CardPrice.price_date == latest_price_subquery.c.latest_price_date)
        )
        .join(Card, CardPrice.card_id == Card.id)
        .group_by(Card.name, Card.id)
        .all()
    )

    price_dict = {}
    for name, id, price in lowest_prices:
        price_dict[name.lower()] = {
            'name': name,
            'price': price,
            'id': id
        }

    return price_dict

def get_card_by_id(card_id):
    return db.session.query(Card).filter_by(id=card_id).first()

def get_card_prices_by_id(card_id):
    return db.session.query(CardPrice).filter_by(card_id=card_id).all()
