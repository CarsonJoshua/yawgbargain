
from sqlalchemy import func
from .models import Card, CardPrice



def get_latest_prices(card_names):
    """Fetches the latest price for each card in the given list of names."""
    if not card_names:
        return {}
    
    

    cards = Card.query.filter(Card.name.in_(card_names)).all()
    card_id_map = {card.name: card.id for card in cards}

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

    # Combine card IDs with the lowest prices
    price_dict = {}
    for name, price in lowest_prices:
        price_dict[name] = {
            'lowest_price': price,
            'card_id': card_id_map.get(name)  # Get the card ID from the map
        }

    return price_dict
