from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from modelo import db #Reminder de inicializar solo una vez SQLAlchemy
from routes.productos import productos_bp
from routes.usuarios import usuarios_bp
from routes.pedidos import pedido_bp



# Crear la aplicación Flask
app = Flask(__name__)

# Cargar la configuración desde config.py
app.config.from_object(Config)

# Asociar SQLAlchemy con la aplicación Flask
db.init_app(app)

#BLUEPRINTS
app.register_blueprint(productos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(pedido_bp)

@app.route('/')
def home():
    return "Bienvenido a la API de MiniShop"
# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
