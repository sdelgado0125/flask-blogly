"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://img.icons8.com/?size=100&id=23265&format=png&color=000000"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False,
                     unique=True)
    last_name = db.Column(db.String(50),
                     nullable=False,
                     unique=True)
    image_url = db.Column(db.Text, 
                          nullable=False, 
                          default=DEFAULT_IMAGE_URL)
    
    def __repr__(self):
        return f'<User {self.id} {self.first_name} {self.last_name}>'
    