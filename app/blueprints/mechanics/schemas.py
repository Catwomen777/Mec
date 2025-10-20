from app.extensions import ma
from app.models import Mechanic


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True  # optional, include if model has foreign keys
        ordered = True     # keeps fields in the same order as your model definition


# Single and multiple serializers
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
