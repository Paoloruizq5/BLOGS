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

@posts_bp.route('/post/new', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category_id = request.form.get('category_id')
        new_post = Post(title=title, content=content, category_id=category_id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('posts.listar_posts'))
    
    categories = Category.query.all()
    return render_template('posts/create_posts.html', categories=categories)  # Cambiado a incluir la subcarpeta posts