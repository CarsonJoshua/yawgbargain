from ..dao import db
from sqlalchemy import UUID

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True) #TODO may need to add UUID generation
    ##TODO probably need to flesh out the rest of the user stuff, will worry about that after security
   