"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    
    posts = db.relationship('Post', backref = 'user', cascade = 'all,delete-orphan')
    
    def __repr__(self):
        return f'<User {self.id} {self.first_name} {self.last_name}>'
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.Text,
                    nullable=False,
                    unique=True)
    content = db.Column(db.Text,
                    nullable=False)
    created_at = db.Column(db.DateTime, 
                    default=datetime.utcnow, 
                    nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        nullable = False)
    
    @property
    def friendly_date(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')