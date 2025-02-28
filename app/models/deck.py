from ..dao import db
from sqlalchemy import UUID, Enum
from .format import Format

class Deck(db.Model):
    __tablename__ = "decks"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), index = True)
    format = db.Column(Enum(Format), nullable = False)
    description = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Deck {self.id}>"