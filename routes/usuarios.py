# routes/usuarios.py
from flask import Blueprint, request, jsonify
from modelo import db, Usuario

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuario', methods=['POST'])
def crear_usuario():
    try:
        data = request.json

        # Validar datos obligatorios
        nombre = data.get('nombre_usuario')
        email = data.get('email')

        if not nombre or not email:
            return jsonify({"status": "error", "message": "Nombre y email son obligatorios"}), 400

        # Verificar si el usuario ya existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return jsonify({
                "status": "ok",
                "message": "Usuario ya existe",
                "usuario": {
                    "id_usuario": usuario_existente.id_usuario,
                    "nombre_usuario": usuario_existente.nombre_usuario,
                    "email": usuario_existente.email
                }
            }), 200

        # Crear nuevo usuario
        nuevo_usuario = Usuario(nombre_usuario=nombre, email=email)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({
            "status": "ok",
            "message": "Usuario creado con éxito",
            "usuario": {
                "id_usuario": nuevo_usuario.id_usuario,
                "nombre_usuario": nuevo_usuario.nombre_usuario,
                "email": nuevo_usuario.email
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
