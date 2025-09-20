from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from routes.productos import productos_bp


#Inicializar SQLAlchemy
db = SQLAlchemy()

# Crear la aplicación Flask
app = Flask(__name__)

# Cargar la configuración desde config.py
app.config.from_object(Config)

# Asociar SQLAlchemy con la aplicación Flask
db.init_app(app)

#BLUEPRINTS
app.register_blueprint(productos_bp)

@app.route('/')
def home():
    return "Bienvenido a la API de MiniShop"
# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
