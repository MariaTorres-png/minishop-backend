from flask_sqlalchemy import SQLAlchemy

#Inicializar SQLAlchemy
db = SQLAlchemy()

class Producto(db.Model):
    __tablename__ = 'productos'
    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_producto = db.Column(db.String(100), nullable=False)
    imagen_url = db.Column(db.Text, nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_usuario = db.Column(db.String(200), nullable=False)
    email = db.Column(db.Text, nullable=False)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_pedido = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('pedidos', lazy=True))


class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedido'
    id_detalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    pedido = db.relationship('Pedido', backref=db.backref('detalles_pedido', lazy=True))
    producto = db.relationship('Producto')