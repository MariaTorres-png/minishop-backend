from flask import Blueprint, request, jsonify
from modelo import db, Pedido, DetallePedido, Usuario
from datetime import datetime
from decimal import Decimal

pedido_bp = Blueprint('pedido', __name__)

@pedido_bp.route('/pedido', methods=['POST'])
def crear_pedido():
    data = request.get_json()

    try:
        # 1️⃣ Validar datos obligatorios
        nombre = data.get("nombre_usuario")
        email = data.get("email")
        detalles = data.get("detalles", [])
        total_enviado = data.get("total")

        if not nombre or not email or not total_enviado:
            return jsonify({"error": "Nombre, email y total son obligatorios"}), 400

        # 2️⃣ Validar o crear usuario
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            usuario = Usuario(nombre_usuario=nombre, email=email)
            db.session.add(usuario)
            db.session.flush()

        # 3️⃣ Validar total
        total_enviado = Decimal(str(total_enviado)).quantize(Decimal("0.01"))
        total_calculado = sum(
            Decimal(str(item["cantidad"])) * Decimal(str(item["precio_unitario"]))
            for item in detalles
        ).quantize(Decimal("0.01"))

        if total_enviado != total_calculado:
            return jsonify({
                "error": "El total no coincide",
                "total_enviado": str(total_enviado),
                "total_calculado": str(total_calculado)
            }), 400

        # 4️⃣ Crear pedido
        nuevo_pedido = Pedido(
            id_usuario=usuario.id_usuario,
            fecha_pedido=datetime.utcnow(),
            total=total_calculado
        )
        db.session.add(nuevo_pedido)
        db.session.flush()

        # 5️⃣ Crear detalles
        for item in detalles:
            nuevo_detalle = DetallePedido(
                id_pedido=nuevo_pedido.id_pedido,
                id_producto=item["id_producto"],
                cantidad=item["cantidad"],
                precio_unitario=item["precio_unitario"]
            )
            db.session.add(nuevo_detalle)

        db.session.commit()

        return jsonify({
            "message": "Pedido creado exitosamente",
            "pedido_id": nuevo_pedido.id_pedido,
            "total_calculado": str(total_calculado)
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
