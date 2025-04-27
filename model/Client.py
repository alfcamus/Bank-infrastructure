class Client:
    def __init__(self, id, name, surname, pesel, accounts, login, password):
        self.id = id
        self.name = name
        self.pesel = pesel
        self.accounts = accounts
        self.login = login
        self.password = password
        self.surname = surname

    def to_dict(self):
        return {'name': self.name, "surname": self.surname, "id": self.id, "pesel": self.pesel, "accounts": [account.to_dict() for account in self.accounts], "login" : self.login}
    
    def to_db(self):
        return {'name': self.name, "surname": self.surname, "pesel": self.pesel, "login" : self.login, "password": self.password}