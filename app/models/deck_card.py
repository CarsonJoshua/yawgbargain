from ..extensions import db
from sqlalchemy import UUID, Enum
from .zone import Zone

class DeckCard(db.Model):
    __tablename__ = "deck_cards"

    id = db.Column(UUID(as_uuid=True), db.ForeignKey("cards.id"), primary_key=True)
    deck_id = db.Column(UUID(as_uuid=True), db.ForeignKey("decks.id"), primary_key=True, index = True)
    count = db.Column(db.Integer(), nullable=False)
    zone = db.Column(Enum(Zone), nullable = False)

    def __repr__(self):
        return f"<DeckCard {self.deck_id}:{self.card_id}>"