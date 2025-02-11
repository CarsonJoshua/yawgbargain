import requests, json, os
from datetime import date
from run import app
from app.extensions import db
from app.models import Card, CardPrice

SCRYFALL_BULK_URL = "https://api.scryfall.com/bulk-data"

def name_position_file(downloadURL):
    return f'position-{downloadURL[downloadURL.rfind('-')+1:downloadURL.find('.json')]}.txt'

def get_download_position(positionFile):
    """Get the last downloaded byte position from the POSITION_FILE."""
    if os.path.exists(positionFile):
        with open(positionFile, "r") as f:
            return int(f.read().strip())
    return 0  # Start from the beginning if the file doesn't exist

def save_download_position(positionFile, position):
    """Save the current download byte position to the POSITION_FILE."""
    with open(positionFile, "w") as f:
        f.write(str(position))

def fetch_bulk_price_url():
    """Fetch the URL for the latest price bulk data file."""
    response = requests.get(SCRYFALL_BULK_URL)
    if response.status_code != 200:
        raise Exception("Failed to fetch bulk data index.")
    
    for entry in response.json()['data']:
        if entry['type'] == 'default_cards':
            return entry['download_uri']
    
    raise Exception("Price bulk data not found.")

def update_card_prices():
    today = date.today()
    downloadURL = fetch_bulk_price_url()
    positionFile = name_position_file(downloadURL=downloadURL)
    downloaded_bytes = get_download_position(positionFile=positionFile)

    headers = {}
    if downloaded_bytes > 0:
        headers["Range"] = f"bytes={downloaded_bytes}-"

    with requests.get(downloadURL, stream=True, headers=headers) as response:
        if response.status_code != 200:
            raise Exception("Failed to download price data.")
        
        for line in response.iter_lines():
            downloaded_bytes += len(line)
            if line == b'[' or line == b']':
                save_download_position(positionFile=positionFile, position=downloaded_bytes)
                continue
            try:
                if line[-1]==ord(','):
                    line = line[:-1]
                card_info = json.loads(line)
                """Add card to db if not in db"""
                if not Card.query.filter_by(id=card_info.get("id")).first():
                    db.session.add(Card(id=card_info.get("id"),name=card_info.get("name")))
                """Add price to db if not in db"""
                if not CardPrice.query.filter_by(card_id=card_info.get("id"), price_date=today).first() and card_info.get("prices").get("usd"):
                    db.session.add(CardPrice(card_id=card_info.get("id"), price_date=today, price=card_info.get("prices").get("usd")))
                
                db.session.commit()
                save_download_position(positionFile=positionFile, position=downloaded_bytes)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}\n Line: {line}")
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        update_card_prices()
