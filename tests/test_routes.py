import unittest
from service import app
from service.models import store


class TestAccountRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        store.clear()

    def test_index(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_crud_flow(self):
        payload = {"name": "Charlie Day", "email": "charlie@example.com", "address": "789 Pine Rd", "phone_number": "555-0199"}
        create_resp = self.client.post("/accounts", json=payload)
        self.assertEqual(create_resp.status_code, 201)
        acc_id = create_resp.get_json()["id"]
        self.assertEqual(self.client.get(f"/accounts/{acc_id}").status_code, 200)
        self.assertEqual(len(self.client.get("/accounts").get_json()), 1)
        upd = self.client.put(f"/accounts/{acc_id}", json={"name": "Charlie Kelly", "email": "charlie@example.com", "address": "789 Pine Rd"})
        self.assertEqual(upd.status_code, 200)
        self.assertEqual(self.client.delete(f"/accounts/{acc_id}").status_code, 204)

    def test_security_and_cors_headers(self):
        resp = self.client.get("/accounts", headers={"Origin": "[http://example.com](http://example.com)"})
        self.assertIn("X-Frame-Options", resp.headers)
        self.assertIn("Access-Control-Allow-Origin", resp.headers)
