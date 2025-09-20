from flask import Blueprint, request, jsonify
from modelo import db, Producto  # Importar el modelo Producto y db

# Crear un Blueprint para las rutas de productos
productos_bp = Blueprint('productos_bp', __name__)

# Obtener todos los productos (GET)
@productos_bp.route('/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()  # Obtener todos los productos de la base de datos
    productos_list = [{
        'id_producto': p.id_producto,
        'nombre_producto': p.nombre_producto,
        'imagen_url': p.imagen_url,
        'descripcion': p.descripcion,
        'precio': p.precio,
        'activo': p.activo
    } for p in productos]
    return jsonify(productos_list)

# Crear un nuevo producto (POST)
@productos_bp.route('/productos', methods=['POST'])
def create_producto():
    data = request.get_json()  # Obtener los datos en formato JSON
    nombre_producto = data.get('nombre_producto')
    precio = data.get('precio')
    imagen_url = data.get('imagen_url')
    descripcion = data.get('descripcion')
    activo = data.get('activo', True)  # Si no se especifica, por defecto se marca como activo

    # Validación de campos
    if not nombre_producto or not precio:
        return jsonify({'message': 'El nombre y el precio son obligatorios'}), 400

    # Crear el nuevo producto
    nuevo_producto = Producto(
        nombre_producto=nombre_producto,
        precio=precio,
        imagen_url=imagen_url,
        descripcion=descripcion,
        activo=activo
    )

    # Agregar a la base de datos
    db.session.add(nuevo_producto)
    db.session.commit()

    return jsonify({
        'id_producto': nuevo_producto.id_producto,
        'nombre_producto': nuevo_producto.nombre_producto,
        'precio': nuevo_producto.precio,
        'imagen_url': nuevo_producto.imagen_url,
        'descripcion': nuevo_producto.descripcion,
        'activo': nuevo_producto.activo
    }), 201  # Código de éxito para creación

# Eliminar un producto (DELETE)
@productos_bp.route('/productos/<int:id_producto>', methods=['DELETE'])
def delete_producto(id_producto):
    producto = Producto.query.get(id_producto)
    if not producto:
        return jsonify({'message': 'Producto no encontrado'}), 404

    # Eliminar el producto
    db.session.delete(producto)
    db.session.commit()

    return jsonify({'message': 'Producto eliminado exitosamente'})

# Actualizar un producto (PUT)
@productos_bp.route('/productos/<int:id_producto>', methods=['PUT'])
def update_producto(id_producto):
    producto = Producto.query.get(id_producto)
    if not producto:
        return jsonify({'message': 'Producto no encontrado'}), 404

    data = request.get_json()

    producto.nombre_producto = data.get('nombre_producto', producto.nombre_producto)
    producto.precio = data.get('precio', producto.precio)
    producto.imagen_url = data.get('imagen_url', producto.imagen_url)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.activo = data.get('activo', producto.activo)

    db.session.commit()

    return jsonify({
        'id_producto': producto.id_producto,
        'nombre_producto': producto.nombre_producto,
        'precio': producto.precio,
        'imagen_url': producto.imagen_url,
        'descripcion': producto.descripcion,
        'activo': producto.activo
    })
