"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from traitlets import default

db = SQLAlchemy()

default_url ="https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/cute-photos-of-cats-excited-1593184777.jpg?crop=1xw:1xh;center,top&resize=768:*"
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
   
    def delete_user(self, id):
        return self.query.filter_by(id=self.id).delete()


    def edit_user(self, id):
        return self.query.filter(id==id).delete()

