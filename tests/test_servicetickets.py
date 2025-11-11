import unittest
from app import create_app
from app.extensions import db


class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        
        self.customer = self.client.post("/customers/customers", json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "1234567890",
            "password": "secret123"
        }).json

        
        self.mechanic = self.client.post("/mechanics", json={
            "name": "Mike Ross",
            "email": "mike@shop.com",
            "salary": 60000
        }).json

        
        self.ticket = self.client.post("/service_tickets/", json={
            "customer_id": self.customer["id"],
            "service_description": "Brake Inspection"
        }).json

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

   
    def test_create_ticket(self):
        res = self.client.post("/service_tickets/", json={
            "customer_id": self.customer["id"],
            "service_description": "Oil change"
        })
        self.assertEqual(res.status_code, 201)
        self.assertIn("id", res.json)

    
    def test_list_tickets(self):
        res = self.client.get("/service_tickets/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json, list)

    
    def test_get_ticket(self):
        res = self.client.get(f"/service_tickets/{self.ticket['id']}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["id"], self.ticket["id"])

    
    def test_update_ticket(self):
        res = self.client.put(f"/service_tickets/{self.ticket['id']}", json={
            "service_description": "Updated Brake Check"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["service_description"], "Updated Brake Check")

    def test_delete_ticket(self):
        res = self.client.delete(f"/service_tickets/{self.ticket['id']}")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Service ticket deleted successfully", res.json["message"])

    
    def test_assign_mechanic(self):
        res = self.client.post(
            f"/service_tickets/{self.ticket['id']}/assign_mechanic",
            json={"mechanic_id": self.mechanic["id"]}
        )
        self.assertEqual(res.status_code, 200)
        mechanic_ids = [m["id"] for m in res.json.get("mechanics", [])]
        self.assertIn(self.mechanic["id"], mechanic_ids)

    
    def test_remove_mechanic(self):
       
        self.client.post(
            f"/service_tickets/{self.ticket['id']}/assign_mechanic",
            json={"mechanic_id": self.mechanic["id"]}
        )
      
        res = self.client.post(
            f"/service_tickets/{self.ticket['id']}/remove_mechanic",
            json={"mechanic_id": self.mechanic["id"]}
        )
        self.assertEqual(res.status_code, 200)
        mechanic_ids = [m["id"] for m in res.json.get("mechanics", [])]
        self.assertNotIn(self.mechanic["id"], mechanic_ids)


if __name__ == "__main__":
    unittest.main()
