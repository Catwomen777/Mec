import unittest
from app import create_app
from app.extensions import db

class TestMechanics(unittest.TestCase):

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

    # ---- CREATE mechanic ----
    def test_create_mechanic(self):
        payload = {
            "name": "Mike Ross",
            "email": "mike.ross@shop.com",
            "salary": 65000
        }

        response = self.client.post("/mechanics", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["name"], "Mike Ross")
        self.assertEqual(response.json["email"], "mike.ross@shop.com")

    # ---- LIST mechanics ----
    def test_list_mechanics(self):
        # create one first
        self.client.post("/mechanics", json={
            "name": "Harvey Specter",
            "email": "harvey@shop.com",
            "salary": 90000
        })
        response = self.client.get("/mechanics")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreaterEqual(len(response.json), 1)

    # ---- GET one mechanic ----
    def test_get_mechanic(self):
        create_res = self.client.post("/mechanics", json={
            "name": "Rachel Zane",
            "email": "rachel@shop.com",
            "salary": 70000
        })
        mechanic_id = create_res.json["id"]

        res = self.client.get(f"/mechanics/{mechanic_id}")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["name"], "Rachel Zane")

    # ---- UPDATE mechanic ----
    def test_update_mechanic(self):
        create_res = self.client.post("/mechanics", json={
            "name": "Donna Paulsen",
            "email": "donna@shop.com",
            "salary": 80000
        })
        mechanic_id = create_res.json["id"]

        update_res = self.client.put(f"/mechanics/{mechanic_id}", json={
            "name": "Donna Updated",
            "email": "donna@shop.com",
            "salary": 85000
        })

        self.assertEqual(update_res.status_code, 200)
        self.assertEqual(update_res.json["name"], "Donna Updated")
        self.assertEqual(update_res.json["salary"], 85000)

    # ---- DELETE mechanic ----
    def test_delete_mechanic(self):
        create_res = self.client.post("/mechanics", json={
            "name": "Louis Litt",
            "email": "litt@shop.com",
            "salary": 60000
        })
        mechanic_id = create_res.json["id"]

        delete_res = self.client.delete(f"/mechanics/{mechanic_id}")

        self.assertEqual(delete_res.status_code, 200)
        self.assertEqual(delete_res.json["message"], "Mechanic deleted successfully")
