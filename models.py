"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from traitlets import default

db = SQLAlchemy()

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
                     default='flask-blogly/image/default.jpg')
   
    def delete_user(self, id):
        return self.query.filter_by(id=id).delete()

        
    def edit_user(self, id):
        return self.query.filter_by(id=id).delete()

