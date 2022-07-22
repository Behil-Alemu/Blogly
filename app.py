"""Blogly application."""

from flask import Flask,render_template, redirect, flash, session,request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db,User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "catladyz97"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def to_user():
    """redirect to user page to show list and form"""
    return redirect('/users')

@app.route('/users')
def list_user():
    """Shows list of all pets in db"""
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def show_form():
    '''show the form to add user'''
    return render_template('form.html')


@app.route('/users', methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    url = request.form["url"]

    new_user  = User(first_name=first_name, last_name=last_name, url=url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')


@app.route("/users/<int:blog_id>")
def show_details(blog_id):
    """Show details about a single User"""
    user = User.query.get_or_404(blog_id)
    return render_template("details.html", user=user)

@app.route("/users/<int:blog_id>/edit")
def show_edit(blog_id):
    user = User.query.get_or_404(blog_id)
    return render_template("edit.html", user=user)

@app.route("/users/<int:blog_id>/delete")
def show_delete(blog_id):
    user_deleted = User.delete_user(blog_id)
    db.session.add(user_deleted)
    db.session.commit()
    return redirect('/users')

