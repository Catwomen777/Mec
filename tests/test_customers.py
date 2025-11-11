import unittest
from app import create_app
from app.extensions import db


class TestCustomerRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TestingConfig")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

        # Create user for auth tests
        self.client.post("/customers/customers", json={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "5551234567",
            "password": "secret123"
        })

    def get_token(self):
        response = self.client.post("/customers/login", json={
            "email": "john@example.com",
            "password": "secret123"
        })

        # Debug print in case login fails
        print("Login Response:", response.json)

        self.assertEqual(response.status_code, 200, "❌ Login failed in get_token()")
        return response.json["token"]

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ---- TEST CREATE ----
    def test_create_customer(self):
        res = self.client.post("/customers/customers", json={
            "name": "Alice",
            "email": "alice@example.com",
            "phone": "1112223333",
            "password": "pass1234"
        })
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json["name"], "Alice")

    # ---- TEST LOGIN ----
    def test_login(self):
        res = self.client.post("/customers/login", json={
            "email": "john@example.com",
            "password": "secret123"
        })
        self.assertEqual(res.status_code, 200)
        self.assertIn("token", res.json)

    # ---- TEST PROTECTED ROUTE WITHOUT TOKEN ----
    def test_get_customer_requires_token(self):
        res = self.client.get("/customers/1")
        self.assertEqual(res.status_code, 401)

    # ---- TEST GET WITH TOKEN ----
    def test_get_customer_with_token(self):
        token = self.get_token()
        res = self.client.get("/customers/1", headers={
            "Authorization": f"Bearer {token}"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["name"], "John Doe")

    # ---- TEST UPDATE ----
    def test_update_customer(self):
        token = self.get_token()
        res = self.client.put("/customers/1", json={
            "name": "John Updated"
        }, headers={
            "Authorization": f"Bearer {token}"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["name"], "John Updated")

    # ---- TEST DELETE ----
    def test_delete_customer(self):
        token = self.get_token()
        res = self.client.delete("/customers/1", headers={
            "Authorization": f"Bearer {token}"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["message"], "Customer deleted successfully.")
