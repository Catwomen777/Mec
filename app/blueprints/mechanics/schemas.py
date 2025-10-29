from app.extensions import ma
from app.models import Mechanic
from marshmallow import fields, validates, ValidationError

class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        load_instance = True
        include_fk = True  # if your Mechanic model has foreign keys
        
   
   
    
        
        
        


# Single and multiple serializers
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
