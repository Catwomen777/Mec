from marshmallow import fields
from app.extensions import ma
from app.models import ServiceTicket
from app.blueprints.customers.schemas import customer_schema
from app.blueprints.mechanics.schemas import mechanic_schema


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    customer = fields.Nested(customer_schema)   
    mechanics = fields.Nested(mechanic_schema, many=True)

    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True


ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
