"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.sql import text
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()

connect_db(app)

@app.route('/')
def list_users(): 
    """ Shows list of all pets in db"""
    with app.app_context():
        users = User.query.all()

    return render_template('list_users.html', users = users)

@app.route('/new')
def show_add_user():

    return render_template('new_user.html')

@app.route('/new', methods=["POST"])
def create_user():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]


    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect (f"/{new_user.id}")
    
@app.route('/<int:user_id>')
def show_user(user_id):
    """Show details about a single user"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.all()

    return render_template("user_details.html",user=user, posts=posts)

@app.route('/<int:user_id>/edit')
def show_edit_user(user_id):

    user = User.query.get_or_404(user_id)

    return render_template("edit_user.html", user=user)

@app.route('/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = User.query.get(user_id)
    user.first_name = f'{first_name}'
    user.last_name= f'{last_name}'
    user.image_url= f'{image_url}'
    db.session.add(user)
    db.session.commit()

    return redirect (f"/{user.id}")
    
@app.route('/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")

@app.route('/<int:user_id>/posts/new')
def show_new_post(user_id):

    user = User.query.get_or_404(user_id)

    return render_template("new_post.html",user=user,)

@app.route('/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    title = request.form["title"]
    content = request.form["content"]

    user = User.query.get(user_id)
    
    new_post = Post(title = title, content = content, user_id = user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/{user.id}")

@app.route('/posts/<int:post_id>')
def show_user_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_first = post.user.first_name
    user_last = post.user.last_name
    user_id = post.user.id

    return render_template("post_details.html", post=post, firstname = user_first, lastname = user_last, user_id = user_id)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_page(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template("edit_post.html", post = post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    title = request.form["title"]
    content = request.form["content"]

    post = Post.query.get(post_id)
    post.title = f'{title}'
    post.content = f'{content}'
    db.session.add(post)
    db.session.commit()

    return redirect (f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):

    post = Post.query.get(post_id)
    
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/{post.user_id}")