from app.extensions import ma
from app.models import InventoryItem


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = InventoryItem
        load_instance = True
        include_fk = True   # include foreign keys if any
        ordered = True      # keep JSON output ordered


inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
