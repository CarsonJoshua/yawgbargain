import requests, json
from datetime import date
from app import db, app
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
    today = date.today()
    """Fetch latest card prices and update the database."""
    response = requests.get(fetch_bulk_price_url(), stream=True)
    if response.status_code != 200:
        raise Exception("Failed to download price data.")
    
    for line in response.iter_lines():
        if line == '[':
            continue
        if line == ']':
            break
        try:
            card_info = json.loads(line)
            """Add card to db if not in db"""
            if not Card.query.filter_by(id=card_info.get("oracle_id")):
                db.session.add(Card(id=card_info.get("oracle_id"),name=card_info.get("name")))
            """Add price to db if not in db"""
            if not CardPrice.query.filter_by(card_id=card_info.get("oracle_id"), price_date=today).first():
                db.session.add(CardPrice(card_id=card_info.get("oracle_id"), price_date=today, price=card_info.get("prices").get("usd")))
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        update_card_prices()
