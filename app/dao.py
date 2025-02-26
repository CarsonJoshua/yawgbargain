from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from app.models.card import Card
from app.models.card_price import CardPrice

db = SQLAlchemy()

def get_latest_prices(card_names):
    """Fetches the latest price for each card in the given list of names."""
    if not card_names:
        return {}

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

    return {name: price for name, price in lowest_prices}
