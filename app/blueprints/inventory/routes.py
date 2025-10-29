from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app.models import InventoryItem   # ✅ Correct model import
from app.blueprints.inventory import inventory_bp
from app.extensions import limiter, cache, db
from .schemas import inventory_schema, inventories_schema


@inventory_bp.route("/", methods=["POST"])
@limiter.limit("5 per minute")
def create_inventory_item():
    data = request.get_json() or {}
    try:
        item = inventory_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.add(item)
    db.session.commit()
    return inventory_schema.jsonify(item), 201


@inventory_bp.route("/", methods=["GET"])
@cache.cached(timeout=30)
def get_inventory_items():
    items = db.session.execute(select(InventoryItem)).scalars().all()  
    return inventories_schema.jsonify(items), 200  


@inventory_bp.route("/<int:item_id>", methods=["GET"])
@cache.cached(timeout=30)
def get_inventory_item(item_id):
    item = db.session.get(InventoryItem, item_id)  
    if not item:
        return jsonify({"error": "Inventory item not found."}), 404
    return inventory_schema.jsonify(item), 200


@inventory_bp.route("/<int:item_id>", methods=["PUT", "PATCH"])
@limiter.limit("5 per minute")
def update_inventory_item(item_id):
    item = db.session.get(InventoryItem, item_id)  # 
    if not item:
        return jsonify({"error": "Inventory item not found."}), 404

    data = request.get_json() or {}
    try:
        item = inventory_schema.load(data, instance=item, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return inventory_schema.jsonify(item), 200


@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
@limiter.limit("20 per day")
def delete_inventory_item(item_id):
    """Delete an inventory item."""
    item = db.session.get(InventoryItem, item_id)
    if not item:
        return jsonify({"error": "Inventory item not found."}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Inventory item deleted successfully."}), 200
