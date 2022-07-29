from app import db

class Card(db.Model):
    __tablename__ = 'cards'
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    artist = db.Column(db.String)
    year = db.Column(db.String)
    img_src = db.Column(db.String)

    board_id = db.Column(db.Integer, db.ForeignKey("boards.board_id"))
    board = db.relationship("Board", back_populates="cards")