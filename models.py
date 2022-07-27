"""Models for Blogly."""
from turtle import title
from flask_sqlalchemy import SQLAlchemy
import datetime
from traitlets import default

db = SQLAlchemy()

default_url ="https://i.insider.com/61d1c0e2aa741500193b2d18?width=1000&format=jpeg&auto=webp"
def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__='blog'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50),
                     nullable=False,
                     unique=True)
    last_name = db.Column(db.String(50),
                     nullable=True,
                    )

    url = db.Column(db.Text,
                     nullable=False,
                     default=default_url)
    posts = db.relationship('Post',backref='user')
   
class Post(db.Model):
    __tablename__='post'    

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=False)
    content= db.Column(db.Text, nullable=False, unique=False)
    created_at=db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('blog.id'))


    # me=Post(title='About me', content='some stuff', created_at='02/29/2022', user= 'check') db.session.add(me) and db.commit() me.user.first_name  check.posts[0]