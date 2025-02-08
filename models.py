import enum
from app import db
from sqlalchemy import UUID, Enum

##ENUMS
class Zone(enum.Enum):
    main = "MAIN"
    side = "SIDE"
    commander = "COMMANDER"

class Format(enum.Enum):
    standard = "STANDARD"
    commander = "COMMANDER"
    hamilton = "HAMILTON"



##TABLES
class CardPrice(db.Model):
    __tablename__ = "card_prices"

    oracle_id = db.Column(UUID(as_uuid=True), db.ForeignKey("cards.oracle_id"), primary_key=True)
    price_date = db.Column(db.Date, primary_key=True, index = True)
    price = db.Column(db.Numeric(10, 2), nullable=False, index = True)  

    ##card = db.relationship("Card", backref="card_prices")##TODO adding relationships may make development more convenient

    def __repr__(self):
        return f"<CardPrice {self.card_id} - {self.price_date}: {self.price}>"


class Card(db.Model):
    __tablename__ = "cards"

    oracle_id = db.Column(UUID(as_uuid=True), primary_key=True, index = True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Card {self.name}>"

#models below will largely go unused until account creation is implemented

class Deck(db.Model):
    __tablename__ = "decks"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), index = True)
    format = db.Column(Enum(Format), nullable = False)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Deck {self.id}>"

class DeckCard(db.Model):
    __tablename__ = "deck_cards"

    oracle_id = db.Column(UUID(as_uuid=True), db.ForeignKey("cards.id"), primary_key=True)
    deck_id = db.Column(UUID(as_uuid=True), db.ForeignKey("decks.id"), primary_key=True, index = True)
    count = db.Column(db.Integer(), nullable=False)
    zone = db.Column(Enum(Zone), nullable = False)

    def __repr__(self):
        return f"<DeckCard {self.deck_id}:{self.card_id}>"
    
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True) #TODO may need to add UUID generation
    ##TODO probably need to flesh out the rest of the user stuff, will worry about that after security
    
    

