
from turtle import title
from models import db, connect_db,User,Post,Tag,PostTag
from datetime import datetime
from app import app


# Create all tables
db.drop_all()
db.create_all()



User.query.delete()
Post.query.delete()
Tag.query.delete()
PostTag.query.delete()

first = Post(title='New Car', content='Got a new cat today')
second = Post(title='Black Car', content='Got a Black cat today')

sir = User(first_name ='Sir', last_name='The Cat', url='https://images.unsplash.com/photo-1579168765467-3b235f938439?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8NXx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=60')

skip = User(first_name ='Skip', last_name='Rush', url='https://images.unsplash.com/photo-1571988840298-3b5301d5109b?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8NHx8fGVufDB8fHx8&auto=format&fit=crop&w=500&q=60')



db.session.add_all([first, second, sir, skip])
db.session.commit()