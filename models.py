from app import db

class CardPrice(db.Model):
    __tablename__ = "card_prices"

    card_id = db.Column(db.Integer, db.ForeignKey("cards.id"), primary_key=True)
    price_date = db.Column(db.Date, primary_key=True, index = True)
    price = db.Column(db.Numeric(10, 2), nullable=False, index = True)  

    __table_args__ = (db.Index("idx_card_price_date", "card_id", "price_date"),)

    card = db.relationship("Card", backref="prices")

    def __repr__(self):
        return f"<CardPrice {self.card_id} - {self.price_date}: {self.price}>"


class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True, index = True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Card {self.name}>"
    
class Deck(db.Model):
    __tablename__ = "decks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, primary_key=True)

