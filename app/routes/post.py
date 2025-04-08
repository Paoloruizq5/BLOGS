from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Post, Category

posts_bp = Blueprint('posts', __name__)

# ==================== RUTAS PARA POSTS ====================
@posts_bp.route('/')
def listar_posts():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template('posts/listar_posts.html', posts=posts)

@posts_bp.route('/new', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        category_id = request.form.get('category_id')
        
        if not all([title, content, category_id]):
            flash('Todos los campos son requeridos', 'danger')
            return redirect(url_for('posts.add_post'))
            
        try:
            new_post = Post(title=title, content=content, category_id=category_id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post creado exitosamente!', 'success')
            return redirect(url_for('posts.listar_posts'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    categories = Category.query.all()
    return render_template('posts/create_posts.html', categories=categories)

@posts_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form.get('title', '').strip()
        post.content = request.form.get('content', '').strip()
        post.category_id = request.form.get('category_id')
        
        try:
            db.session.commit()
            flash('Post actualizado', 'success')
            return redirect(url_for('posts.listar_posts'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    categories = Category.query.all()
    return render_template('posts/update_posts.html', 
                         post=post,
                         categories=categories)

@posts_bp.route('/delete/<int:id>', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Post eliminado', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('posts.listar_posts'))

# ==================== RUTAS PARA CATEGORÍAS ====================
@posts_bp.route('/categories')
def list_categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template('posts/categories.html', categories=categories)

@posts_bp.route('/categories/new', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('Nombre requerido', 'danger')
            return redirect(url_for('posts.add_category'))
        
        try:
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            flash('Categoría creada!', 'success')
            return redirect(url_for('posts.list_categories'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: Ya existe una categoría con ese nombre', 'danger')
    
    return render_template('posts/add_category.html')

@posts_bp.route('/categories/<int:id>/delete', methods=['POST'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    try:
        db.session.delete(category)
        db.session.commit()
        flash('Categoría eliminada', 'success')
    except Exception as e:
        db.session.rollback()
        flash('No se puede eliminar: hay posts asociados', 'danger')
    
    return redirect(url_for('posts.list_categories'))