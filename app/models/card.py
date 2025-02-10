from ..extensions import db
from sqlalchemy import UUID

class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(UUID(as_uuid=True), primary_key=True, index = True)
    name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Card {self.name}>"