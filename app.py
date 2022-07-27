"""Blogly application."""

from crypt import methods
from flask import Flask,render_template, redirect, flash, session,request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db,User,Post
from datetime import datetime

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
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def show_form():
    '''show the form to add user'''
    return render_template('form.html')


@app.route('/users', methods=["POST"])
def add_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    url = request.form["url"] or "https://i.insider.com/61d1c0e2aa741500193b2d18?width=1000&format=jpeg&auto=webp"

    new_user  = User(first_name=first_name, last_name=last_name, url=url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')


@app.route("/users/<int:blog_id>")
def show_details(blog_id):
    """Show details about a single User"""
    user = User.query.get_or_404(blog_id)
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("details.html", user=user,posts=posts)

@app.route("/users/<int:blog_id>/edit")
def show_edit(blog_id):
    user = User.query.get_or_404(blog_id)
    return render_template("edit.html", user=user)

@app.route("/users/<int:blog_id>/edit", methods=["POST"])
def save_changes(blog_id):
    user = User.query.get_or_404(blog_id)
    user.first_name= request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.url = request.form["url"] or "https://i.insider.com/61d1c0e2aa741500193b2d18?width=1000&format=jpeg&auto=webp"

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route("/users/<int:blog_id>/delete", methods=["POST"])
def show_delete(blog_id):
    user = User.query.get_or_404(blog_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route("/users/<int:blog_id>/posts/new")
def show_post_form(blog_id):
    user = User.query.get_or_404(blog_id)
    return render_template("post_form.html", user=user)


@app.route("/users/<int:blog_id>/posts/new", methods=["POST"] )
def submit_post_form(blog_id):
    user = User.query.get_or_404(blog_id)
    title= request.form["title"]
    content = request.form["content"]
    posts= Post(title=title,content=content, user=user)

    db.session.add(posts)
    db.session.commit()
    flash(f"Post '{posts.title}' added.")
    return redirect(f'/users/{blog_id}')

@app.route("/posts/<int:post_id>")
def show_added_post(post_id):
    posts = Post.query.get_or_404(post_id)
    return render_template("post_details.html",posts=posts)


@app.route("/post/<int:post_id>/edit")
def edit_post_form(post_id):
    posts = Post.query.get_or_404(post_id)
    return render_template("post_edit_form.html",posts=posts, )


@app.route("/post/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    posts = Post.query.get_or_404(post_id)
    posts.title= request.form["title"]
    posts.content = request.form["content"]

    db.session.add(posts)
    db.session.commit()
    flash(f"Post '{posts.title}' edited.")
    return redirect(f'/posts/{post_id}')


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')


@app.route("/posts/<int:post_id>/cancel", methods=["POST"])
def cancel_post(post_id):
    return redirect(f'/posts/{post_id}')

