import requests, json, app
from datetime import date
from app import db
from models import Card, CardPrice

SCRYFALL_BULK_URL = "https://api.scryfall.com/bulk-data"

def fetch_bulk_price_url():
    """Fetch the URL for the latest price bulk data file."""
    response = requests.get(SCRYFALL_BULK_URL)
    if response.status_code != 200:
        raise Exception("Failed to fetch bulk data index.")
    
    for entry in response.json()['data']:
        if entry['type'] == 'oracle_cards':
            return entry['download_uri']
    
    raise Exception("Price bulk data not found.")

def update_card_prices():
    """Fetch latest card prices and update the database."""
    
    response = requests.get(fetch_bulk_price_url(), stream=True)
    if response.status_code != 200:
        raise Exception("Failed to download price data.")

    price_data = response.json()

    for card_info in price_data:
        if not Card.query.filter_by(id=card_info.get("id")):
            db.session.add(Card(id=card_info.get("id"),name=card_info.get("name")))
            db.session.commit()
        

        return



        # card_name = card_info.get("name")
        # price = card_info.get("prices", {}).get("usd")  # Get USD price

        # if card_name and price:
        #     # Check if card exists in the DB
        #     card = Card.query.filter_by(name=card_name).first()

        #     if not card:
        #         # Add new card to the DB
        #         card = Card(name=card_name)
        #         db.session.add(card)
        #         db.session.commit()
        #         print(f"Added new card: {card_name}")

        #     # Check if a price already exists for today
        #     today = date.today()
        #     existing_price = CardPrice.query.filter_by(card_id=card.id, price_date=today).first()
        #     if not existing_price:
        #         # Insert price into `card_prices`
        #         new_price = CardPrice(card_id=card.id, price_date=today, price=price)
        #         db.session.add(new_price)
        #         db.session.commit()
        #         print(f"Added price for {card_name}: ${price}")

if __name__ == "__main__":
    with app.app_context():
        update_card_prices()
