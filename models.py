"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

default_url ="https://i.insider.com/61d1c0e2aa741500193b2d18?width=1000&format=jpeg&auto=webp"


class User(db.Model):
    """Make a table with user info"""
    __tablename__='blog'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=True)

    url = db.Column(db.Text,
                     nullable=False,
                     default=default_url)

    @property
    def full_name(self):
        """Return full name"""
        return f"{self.first_name}{self.last_name}"

    posts = db.relationship('Post',backref='user')
    
   
class Post(db.Model):
    """Post table """
    __tablename__='post'    

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False, unique=False)

    content= db.Column(db.Text, nullable=False, unique=False)

    created_at=db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)

    @property
    def friendly_date(self):
        """Makes the date look user friendly"""
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")


class PostTag(db.Model):
    """Mapping of a Post to a Tag."""

    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer,
                       db.ForeignKey("post.id"),
                       primary_key=True)
    tag_id = db.Column(db.Integer,
                          db.ForeignKey("tag.id"),
                          primary_key=True)

class Tag(db.Model):
    """ Make a tag table"""
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)
    posts = db.relationship('Post', secondary="post_tag", backref='tag',)

def connect_db(app):
    db.app = app
    db.init_app(app)