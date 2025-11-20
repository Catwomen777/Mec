from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app.models import Customer
from . import customers_bp
from .schemas import customer_schema, customers_schema, login_schema
from app.extensions import limiter, cache, ma, db
from app.utils.util import encode_token, token_required


@customers_bp.route('/login', methods=['POST'])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials.get('email')
        password = credentials.get('password')
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()

    if customer and customer.password == password:
        token = encode_token(customer.id)
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "token": token
        }), 200
    else:
        return jsonify({"error": "Invalid email or password."}), 401

@customers_bp.route('/customers', methods=['POST'])
@customers_bp.route('/', methods=['POST'])
@limiter.limit("5 per minute")
def create_customer():
    data = request.get_json() or {}
    try:
        customer = customer_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.add(customer)
    db.session.commit()
    return customer_schema.jsonify(customer), 201


@customers_bp.route('/', methods=['GET'])
def list_customers():
    items = db.session.execute(select(Customer)).scalars().all()
    return customers_schema.jsonify(items), 200


@customers_bp.route('/<int:customer_id>', methods=['GET'])
@cache.cached(timeout=30)
@token_required
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    return customer_schema.jsonify(customer), 200


@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@limiter.limit("3 per minute")
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    data = request.get_json() or {}
    try:
        updated_customer = customer_schema.load(data, instance=customer, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    db.session.commit()
    return customer_schema.jsonify(updated_customer), 200


@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@token_required
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully."}), 200


@customers_bp.route('/search-customers', methods=['GET'])
def search_customers():
    name = request.args.get('name')
    email = request.args.get('email')

    query = select(Customer)
    if name:
        query = query.where(Customer.name.ilike(f'%{name}%'))
    if email:
        query = query.where(Customer.email.ilike(f'%{email}%'))

    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200
