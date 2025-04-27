class Client:
    def __init__(self, id, name, pesel, accounts):
        self.id = id
        self.name = name
        self.pesel = pesel
        self.accounts = accounts

    def to_dict(self):
        return {'name': self.name, "id": self.id, "pesel": self.pesel, "accounts": [account.to_dict() for account in self.accounts]}
    
    def to_db(self):
        return {'name': self.name, "pesel": self.pesel}