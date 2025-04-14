class Account:
    def __init__(self, id: int, balance: float, account_type):
        self.id = id
        self.balance = balance
        self.account_type = account_type

    def __str__(self):
        return f"Account(id='{self.id}', balance={self.balance})"
