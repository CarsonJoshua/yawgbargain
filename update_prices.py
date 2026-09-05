import gzip
import requests, json
from datetime import date
from app import create_app
from app.dao import db
from app.models import Card, CardPrice

SCRYFALL_BULK_URL = "https://api.scryfall.com/bulk-data"
# Scryfall rejects requests without a descriptive User-Agent (returns 400).
REQUEST_HEADERS = {
    "User-Agent": "yawgbargain/1.0 (+https://yawgbargain.com)",
    "Accept": "application/json",
}

def fetch_bulk_price_url():
    """Fetch the URL for the latest price bulk data file."""
    response = requests.get(SCRYFALL_BULK_URL, headers=REQUEST_HEADERS)
    if response.status_code != 200:
        raise Exception("Failed to fetch bulk data index.")

    for entry in response.json()['data']:
        if entry['type'] == 'default_cards':
            return entry['jsonl_download_uri']

    raise Exception("Price bulk data not found.")

def update_card_prices():
    today = date.today()
    downloadURL = fetch_bulk_price_url()

    with requests.get(downloadURL, stream=True, headers=REQUEST_HEADERS) as response:
        if response.status_code != 200:
            raise Exception("Failed to download price data.")

        # The bulk file is gzip-compressed JSON Lines (one card object per line).
        for line in gzip.GzipFile(fileobj=response.raw):
            try:
                card_info = json.loads(line)
                """Add card to db if not in db"""
                if not Card.query.filter_by(id=card_info.get("id")).first():
                    db.session.add(Card(id=card_info.get("id"),name=card_info.get("name")))
                """Add price to db if not in db"""
                if not CardPrice.query.filter_by(card_id=card_info.get("id"), price_date=today).first() and card_info.get("prices").get("usd"):
                    db.session.add(CardPrice(card_id=card_info.get("id"), price_date=today, price=card_info.get("prices").get("usd")))

                db.session.commit()
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}\n Line: {line}")
        db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        update_card_prices()
