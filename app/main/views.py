from flask import render_template, url_for ,flash,redirect
from . import main
from ..models import Permission, Role, User, Post
from sqlalchemy import func
from .. import db


@main.route('/',methods=['GET'])
def home():
    posts = Post.query.order_by(Post.edit_timestamp.desc()).all()
    categories = db.session.query(Post.category, func.count(Post.id)).group_by(Post.category).order_by(func.count(Post.id).desc()).all()
    return render_template('main/home.html', posts=posts,categories=categories)

@main.route('/<category>',methods=['GET'])
def category(category):
    posts = Post.query.filter(Post.category.ilike(category)).order_by(Post.create_timestamp.desc()).all()
    categories = db.session.query(Post.category, func.count(Post.id)).group_by(Post.category).order_by(func.count(Post.id).desc()).all()
    return render_template('main/home.html', posts=posts,categories=categories)

@main.route('/contact',methods=['GET'])
def contact():
    return render_template('main/contact.html')

@main.route('/about',methods=['GET'])
def about():
    categories = db.session.query(Post.category, func.count(Post.id)).group_by(Post.category).order_by(func.count(Post.id).desc()).all()
    return render_template('main/about.html',categories=categories)

@main.route('/blog/<int:id>',methods=['GET'])
def blog(id):
    post = Post.query.filter_by(id = id).first()
    if post is not None: 
        return render_template('main/blog.html',post = post)
    else :
        flash("Can't find blog for ID provided: %d" % (id))
        return redirect(url_for('main.home'))
