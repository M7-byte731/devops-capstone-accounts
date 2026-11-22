from datetime import date
from typing import Dict, List, Optional


class DataValidationError(Exception):
    pass


class Account:
    def __init__(self, name: str, email: str, address: str, phone_number: str = "", date_joined: Optional[date] = None, account_id: Optional[int] = None):
        self.id = account_id
        self.name = name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.date_joined = date_joined or date.today()

    def to_dict(self) -> Dict:
        return {"id": self.id, "name": self.name, "email": self.email, "address": self.address, "phone_number": self.phone_number, "date_joined": self.date_joined.isoformat()}

    def from_dict(self, data: Dict) -> None:
        if not isinstance(data, dict) or not data.get("name") or not data.get("email"):
            raise DataValidationError("Missing required account fields: name and email")
        self.name = data["name"]
        self.email = data["email"]
        self.address = data.get("address", "")
        self.phone_number = data.get("phone_number", "")


class AccountStore:
    def __init__(self):
        self._accounts: Dict[int, Account] = {}
        self._next_id: int = 1

    def clear(self) -> None:
        self._accounts.clear()
        self._next_id = 1

    def create(self, data: Dict) -> Account:
        account = Account(name="", email="", address="", account_id=self._next_id)
        account.from_dict(data)
        self._accounts[self._next_id] = account
        self._next_id += 1
        return account

    def get(self, account_id: int) -> Optional[Account]:
        return self._accounts.get(account_id)

    def list_all(self) -> List[Account]:
        return list(self._accounts.values())

    def update(self, account_id: int, data: Dict) -> Optional[Account]:
        account = self._accounts.get(account_id)
        if not account:
            return None
        account.from_dict(data)
        return account

    def delete(self, account_id: int) -> bool:
        if account_id in self._accounts:
            del self._accounts[account_id]
            return True
        return False


store = AccountStore()
