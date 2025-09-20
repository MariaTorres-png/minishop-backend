from flask import Blueprint, request, jsonify
from modelo import db, Pedido  # importa la tabla Pedido desde tu modelo

pedido_bp = Blueprint('pedido', __name__)

@pedido_bp.route('/pedido', methods=['POST'])
def crear_pedido():
    data = request.get_json()

    try:
        nuevo_pedido = Pedido(
            usuario_id=data.get("usuario_id"),
            fecha=data.datetime.now(),       # o datetime.now() si lo generas en el backend
            total=data.get("total")
        )

        db.session.add(nuevo_pedido)
        db.session.commit()

        return jsonify({
            "message": "Pedido creado exitosamente",
            "pedido_id": nuevo_pedido.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
