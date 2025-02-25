from ..dao import db
from sqlalchemy import UUID

class CardPrice(db.Model):
    __tablename__ = "card_prices"

    card_id = db.Column(UUID(as_uuid=True), db.ForeignKey("cards.id"), primary_key=True)
    price_date = db.Column(db.Date, primary_key=True, index = True)
    price = db.Column(db.Numeric(10, 2), nullable=False, index = True)  

    ##card = db.relationship("Card", backref="card_prices")##TODO adding relationships may make development more convenient

    def __repr__(self):
        return f"<CardPrice {self.card_id} - {self.price_date}: {self.price}>"