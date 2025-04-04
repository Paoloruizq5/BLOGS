from app import db

# Modelo Categoría
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    nane = db.Column(db.String(100), nullable=False, unique=True)