from flask import request, jsonify
from sqlalchemy import select
from app.extensions import db, limiter, cache
from app.models import ServiceTicket
from . import service_tickets_bp
from .schemas import ticket_schema, tickets_schema
from marshmallow import ValidationError


@service_tickets_bp.route("/", methods=["POST"])
@limiter.limit("10 per minute")
def create_ticket():
    """Create a new service ticket."""
    data = request.get_json() or {}
    try:
        ticket = ticket_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(ticket)
    db.session.commit()
    return ticket_schema.jsonify(ticket), 201


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
