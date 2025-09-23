from flask import Blueprint, request, jsonify
from modelo import db, Producto, Pedido, DetallePedido
from datetime import datetime

estadisticas_bp = Blueprint('estadisticas', __name__)

@estadisticas_bp.route("/estadisticas/ventas", methods=["GET"])
def estadisticas_ventas():
    try:
        fecha_inicio = request.args.get("fecha_inicio")
        fecha_fin = request.args.get("fecha_fin")

        if not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Debes proporcionar fecha_inicio y fecha_fin"}), 400

        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido. Usa YYYY-MM-DD"}), 400

        # --- 1) TOP PRODUCTOS ---
        top_productos = (
            db.session.query(
                Producto.nombre_producto,
                db.func.sum(DetallePedido.cantidad).label("total_vendido"),
                db.func.sum(DetallePedido.cantidad * DetallePedido.precio_unitario).label("total_dinero")
            )
            .join(DetallePedido, DetallePedido.id_producto == Producto.id_producto)
            .join(Pedido, Pedido.id_pedido == DetallePedido.id_pedido)
            .filter(Pedido.fecha_pedido.between(fecha_inicio, fecha_fin))
            .group_by(Producto.id_producto, Producto.nombre_producto)
            .order_by(db.desc("total_vendido"))
            .limit(5)
            .all()
        )

        top_productos_json = [
            {
                "producto": r[0],
                "total_vendido": int(r[1]),
                "total_dinero": float(r[2])
            }
            for r in top_productos
        ]

        # --- 2) VENTAS POR DÍA ---
        ventas_por_dia = (
            db.session.query(
                db.func.date(Pedido.fecha_pedido).label("fecha"),
                db.func.sum(DetallePedido.cantidad * DetallePedido.precio_unitario).label("total_dinero")
            )
            .join(DetallePedido, DetallePedido.id_pedido == Pedido.id_pedido)
            .filter(Pedido.fecha_pedido.between(fecha_inicio, fecha_fin))
            .group_by(db.func.date(Pedido.fecha_pedido))
            .order_by(db.asc("fecha"))
            .all()
        )

        ventas_por_dia_json = [
            {
                "fecha": r[0].strftime("%Y-%m-%d"),
                "total_dinero": float(r[1])
            }
            for r in ventas_por_dia
        ]

        return jsonify({
            "status": "ok",
            "top_productos": top_productos_json,
            "ventas_por_dia": ventas_por_dia_json
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
