from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app.models import Mechanic, db
from app.blueprints.mechanics import mechanics_bp
from app.extensions import limiter, cache
from . import schemas
import inspect
print(f"✅ USING SCHEMA FILE: {inspect.getfile(schemas)}")

from .schemas import mechanic_schema, mechanics_schema



@mechanics_bp.route('', methods=["POST"])
@limiter.limit("3 per minute")
def create_mechanic():
    """Create a new mechanic"""
    data = request.get_json() or {}
    try:
        mechanic = mechanic_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201


@mechanics_bp.route('', methods=["GET"])
def list_mechanics():
    """List all mechanics"""
    items = db.session.execute(select(Mechanic)).scalars().all()
    return mechanics_schema.jsonify(items), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=["GET"])
@cache.cached(timeout=30)
def get_mechanic(mechanic_id):
    """Retrieve one mechanic by id"""
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=["PUT", "PATCH"])
@limiter.limit("5 per minute")
def update_mechanic(mechanic_id):
    """Update a mechanic (partial updates allowed)"""
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    data = request.get_json() or {}
    try:
        mechanic = mechanic_schema.load(data, instance=mechanic, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=["DELETE"])
@limiter.limit("20 per day")
def delete_mechanic(mechanic_id):
    """Delete a mechanic"""
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted successfully"}), 200
