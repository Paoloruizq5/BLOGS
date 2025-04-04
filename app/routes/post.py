from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Post
from app.models import Category

posts_bp = Blueprint ('posts',__name__)

@posts_bp.route('/')
def listar_posts():
    posts = Post.query.all()
    categories = Category.query.all()
    return render_template('posts/listar_posts.html', posts=posts, categories=categories)