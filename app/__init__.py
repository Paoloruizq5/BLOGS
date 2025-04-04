import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv 

# Inicializar extensiones
db = SQLAlchemy()

# Cargar variables de entorno
load_dotenv()

#crear instancia
app =  Flask(__name__)

    
    # Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:paolo5@localhost:5432/postgres')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
db = SQLAlchemy(app)

#Importar modelos para que SQLAlchemy los reconozca
from app.models import Post

#Importar y registrar blueprints
from app.routes.post import posts_bp

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

app.register_blueprint(posts_bp, url_prefix='/posts')

#Ruta principal home
@app.route('/')
def index():
    return 'Hola mundo'