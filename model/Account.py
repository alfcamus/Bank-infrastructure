class Account:
    def __init__(self, id: str, balance: float, account_type, created_at, client_id):
        self.id = id
        self.balance = balance
        self.account_type = account_type
        self.created_at = created_at
        self.client_id = client_id

    def __str__(self):
        return f"Account(id='{self.id}', balance={self.balance})"

    def to_db(self):
        return {'balance': self.balance, "account_type": self.account_type, "client_id": self.client_id}
    
    def to_dict(self):
        return {'balance': self.balance, "id": self.id, "account_type": self.account_type}
