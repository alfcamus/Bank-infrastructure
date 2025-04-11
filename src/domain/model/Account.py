class Account:
    def __init__(self, id: int, balance: float):
        self.id = id
        self.balance = balance

    def __str__(self):
        return f"Account(id='{self.id}', balance={self.balance})"
