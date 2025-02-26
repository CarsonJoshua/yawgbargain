from flask import Blueprint, render_template, request
from ..dao import get_latest_prices
import re

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

        card_names = [name for _, name in card_entries]
        lowest_price_dict = get_latest_prices(card_names)

        deck_prices = []
        for amount, name in card_entries:
            price_info = lowest_price_dict.get(name)
            if price_info:
                price = price_info['lowest_price']
                card_id = price_info['card_id']
                deck_prices.append((amount, card_id, name, price if price is not None else "Price not found"))
            else:
                deck_prices.append((amount, None, name, "Card not found"))

        total_price = sum(
            amount * (price if not isinstance(price, str) else 0) 
            for amount, _, _, price in deck_prices
        )

        return render_template('pricer.html', deck_list=deck_list, deck_prices=deck_prices, total_price=total_price)

    return render_template('pricer.html')

