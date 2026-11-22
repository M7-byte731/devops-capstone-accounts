import unittest
from service.models import AccountStore, DataValidationError


class TestAccountModel(unittest.TestCase):
    def setUp(self):
        self.store = AccountStore()
        self.store.clear()

    def test_create_and_get_account(self):
        acc = self.store.create({"name": "Alice Smith", "email": "alice@example.com", "address": "123 Main St", "phone_number": "555-0100"})
        self.assertEqual(acc.id, 1)
        self.assertEqual(self.store.get(1).email, "alice@example.com")

    def test_create_account_missing_fields(self):
        with self.assertRaises(DataValidationError):
            self.store.create({"name": "Incomplete"})

    def test_update_and_delete_account(self):
        self.store.create({"name": "Bob Jones", "email": "bob@example.com", "address": "456 Oak Ave"})
        updated = self.store.update(1, {"name": "Bob Updated", "email": "bob.updated@example.com", "address": "456 Oak Ave"})
        self.assertEqual(updated.name, "Bob Updated")
        self.assertTrue(self.store.delete(1))
        self.assertIsNone(self.store.get(1))
