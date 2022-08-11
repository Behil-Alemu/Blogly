"""Blogly application."""

from crypt import methods
from flask import Flask,render_template, redirect, flash,request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db,User,Post,Tag
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "catladyz97"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def to_user():
    """redirect to user page to show list and form"""
    return redirect('/users')

@app.route('/users')
def list_user():
    """Shows list of all  users in blogly db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user/list.html', users=users)


@app.route('/users/new')
def show_form():
    '''show the form to add user'''
    return render_template('user/form.html')



@app.route('/users/new', methods=["POST"])
def add_user():
    """Handle submitting a new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    url = request.form["url"] or "https://i.insider.com/61d1c0e2aa741500193b2d18?width=1000&format=jpeg&auto=webp"

    new_user  = User(first_name=first_name, last_name=last_name, url=url)
    db.session.add(new_user)
    db.session.commit()
    flash(f"{new_user.first_name} added!" )

    return redirect('/users')


@app.route("/users/<int:blog_id>")
def show_details(blog_id):
    """Show details about a single User"""
    user = User.query.get_or_404(blog_id)
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("user/details.html", user=user,posts=posts)

@app.route("/users/<int:blog_id>/edit")
def show_edit(blog_id):
    """Show form to edit current user information"""
    user = User.query.get_or_404(blog_id)
    return render_template("user/edit.html", user=user)

@app.route("/users/<int:blog_id>/edit", methods=["POST"])
def save_changes(blog_id):
    """Handle submitting a edit form"""
    user = User.query.get_or_404(blog_id)
    user.first_name= request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.url = request.form["url"] or "https://i.insider.com/61d1c0e2aa741500193b2d18?width=1000&format=jpeg&auto=webp"

    db.session.add(user)
    db.session.commit()
    flash(f"{user.first_name} edited!" )
    return redirect('/users')

@app.route("/users/<int:blog_id>/delete", methods=["POST"])
def show_delete(blog_id):
    """Delete User"""
    user = User.query.get_or_404(blog_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"{user.first_name} deleted" )
    return redirect('/users')

#####################################################POST
@app.route("/users/<int:blog_id>/posts/new")
def show_post_form(blog_id):
    """Show a form to add a new post"""
    user = User.query.get_or_404(blog_id)
    return render_template("post/post_form.html", user=user)


@app.route("/users/<int:blog_id>/posts/new", methods=["POST"] )
def submit_post_form(blog_id):
    """Handle new post submission"""
    user = User.query.get_or_404(blog_id)
    posts= Post(title=request.form["title"],content=request.form["content"], user=user)

    db.session.add(posts)
    db.session.commit()
    flash(f"Post '{posts.title}' added.")
    return redirect(f'/users/{blog_id}')

@app.route("/posts/<int:post_id>")
def show_added_post(post_id):
    """Show detail about the selected post"""
    posts = Post.query.get_or_404(post_id)
    return render_template("post/post_details.html",posts=posts)


@app.route("/post/<int:post_id>/edit")
def edit_post_form(post_id):
    """SHOW esit form"""
    posts = Post.query.get_or_404(post_id)
    return render_template("post/post_edit_form.html",posts=posts, )


@app.route("/post/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Handle edit form submission"""
    posts = Post.query.get_or_404(post_id)
    posts.title= request.form["title"]
    posts.content = request.form["content"]

    db.session.add(posts)
    db.session.commit()
    flash(f"Post '{posts.title}' edited.")
    return redirect(f'/posts/{post_id}')


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Handle delete button for post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"'{post.title}' post deleted" )
    return redirect(f'/users/{post.user_id}')


@app.route("/posts/<int:post_id>/cancel", methods=["POST"])
def cancel_post(post_id):
    """Cancel edit a go back to post info page"""
    return redirect(f'/posts/{post_id}')

####################################################
# TAG


@app.route("/tags")
def list_tag():
    """Show a list of the tags"""
    tags = Tag.query.all()
    return render_template('tag/tag_list.html', tags=tags)

@app.route("/tags/new")
def new_tag_form():
    """show the page to submit a new tag"""
    posts= Post.query.all()
    return render_template('tag/tag_form.html', posts=posts)

@app.route("/tags/new", methods=["POST"])
def submit_tag_form():
    """show the page to submit a new tag"""
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')



@app.route("/tags/<int:tag_id>")
def show_tag_info(tag_id):
    """show Tag detail """
    posts= Post.query.all()
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag/tag_detail.html', tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_info(tag_id):
    """show edit form"""
    posts= Post.query.all()
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag/tag_edit.html", tag=tag, posts=posts)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def submit_tag_edit(tag_id):
    """Handle tag edit submission"""
    new_tags = Tag.query.get_or_404(tag_id)
    new_tags.name= request.form["name"]

    db.session.add(new_tags)
    db.session.commit()
    flash(f"Post '{new_tags.name}' edited.")
    return redirect(f'/tags/{tag_id}')



@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag from the list"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(f'/tags')

# what to understand get list on line 168