from flask import request, jsonify
from sqlalchemy import select
from app.extensions import db, limiter, cache
from app.models import ServiceTicket, Mechanic
from . import service_tickets_bp
from .schemas import ticket_schema, tickets_schema
from marshmallow import ValidationError
import inspect, app.blueprints.servicetickets.schemas as schemas
print(f"✅ USING SCHEMA FILE: {inspect.getfile(schemas)}")



@service_tickets_bp.route("/", methods=["POST"])
@limiter.limit("10 per minute")
def create_service_ticket():
    """Create a service ticket, optionally assigning mechanics."""
    data = request.get_json() or {}

    customer_id = data.get("customer_id")
    description = data.get("service_description")
    mechanic_ids = data.get("mechanic_ids", [])

    if not customer_id or not description:
        return jsonify({"error": "customer_id and service_description are required"}), 400

    # Create the ticket
    ticket = ServiceTicket(
        customer_id=customer_id,
        service_description=description
    )

    # Attach mechanics if provided
    if mechanic_ids:
        mechanics = Mechanic.query.filter(Mechanic.id.in_(mechanic_ids)).all()
        ticket.mechanics.extend(mechanics)

    db.session.add(ticket)
    db.session.commit()

    return jsonify({
        "id": ticket.id,
        "customer_id": ticket.customer_id,
        "service_description": ticket.service_description,
        "mechanic_ids": [m.id for m in ticket.mechanics],
    }), 201



@service_tickets_bp.route("/", methods=["GET"])
@cache.cached(timeout=30, query_string=True)
def list_tickets():
    """List all service tickets."""
    tickets = db.session.execute(select(ServiceTicket)).scalars().all()
    return tickets_schema.jsonify(tickets), 200


@service_tickets_bp.route("/<int:ticket_id>", methods=["GET"])
@cache.cached(timeout=30)
def get_ticket(ticket_id):
    """Retrieve a single service ticket by ID."""
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    return ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route("/<int:ticket_id>", methods=["PUT", "PATCH"])
@limiter.limit("10 per minute")
def update_ticket(ticket_id):
    """Update an existing service ticket."""
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    data = request.get_json() or {}
    try:
        ticket = ticket_schema.load(data, instance=ticket, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()
    return ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route("/<int:ticket_id>", methods=["DELETE"])
@limiter.limit("30 per day")
def delete_ticket(ticket_id):
    """Delete a service ticket by ID."""
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Service ticket deleted successfully"}), 200

@service_tickets_bp.route("/<int:ticket_id>/assign_mechanic", methods=["POST"])
def assign_mechanic(ticket_id):
    data = request.get_json() or {}
    mechanic_id = data.get("mechanic_id")

    if not mechanic_id:
        return jsonify({"error": "mechanic_id is required"}), 400

    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    # Prevent duplicate assignments
    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)

    db.session.commit()

    return ticket_schema.jsonify(ticket), 200

@service_tickets_bp.route("/<int:ticket_id>/remove_mechanic", methods=["POST"])
def remove_mechanic(ticket_id):
    data = request.get_json() or {}
    mechanic_id = data.get("mechanic_id")

    if not mechanic_id:
        return jsonify({"error": "mechanic_id is required"}), 400

    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)

    db.session.commit()

    return ticket_schema.jsonify(ticket), 200
