from app.extensions import ma
from app.models import ServiceTicket


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        include_fk = True     # Include related foreign key fields
        ordered = True        # Keep field order consistent with model definition
        # You can also add: dump_only = ("id",) if you don't want the client to modify ID


ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
