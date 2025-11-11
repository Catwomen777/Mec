import unittest
from app import create_app
from app.extensions import db


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()
            
    def test_create_inventory_item(self):
        payload = {
            "name": "Brake Pads",
            "quantity": 20
        }

        response = self.client.post("/inventory/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Brake Pads")
        self.assertEqual(response.json["quantity"], 20)

    def test_get_inventory_items(self):
        # Create one item first
        self.client.post("/inventory/", json={"name": "Oil Filter", "quantity": 10})

        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json, list))
        self.assertGreaterEqual(len(response.json), 1)

    def test_update_inventory_item(self):
        create = self.client.post("/inventory/", json={"name": "Rotor", "quantity": 5})
        item_id = create.json["id"]

        update = self.client.put(f"/inventory/{item_id}", json={"quantity": 15})
        self.assertEqual(update.status_code, 200)
        self.assertEqual(update.json["quantity"], 15)

    def test_delete_inventory_item(self):
        create = self.client.post("/inventory/", json={"name": "Coolant", "quantity": 3})
        item_id = create.json["id"]

        response = self.client.delete(f"/inventory/{item_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Inventory item deleted successfully.")

        # Verify it was deleted
       

if __name__ == "__main__":
    unittest.main()
