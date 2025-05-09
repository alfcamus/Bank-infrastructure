from service.BaseService import BaseService
from model.Client import Client
import random


class ClientService(BaseService):
    def __init__(self, account_service):
        super().__init__()
        self.account_service = account_service

    def get_client(self, id):
        querry = f"SELECT * FROM clients WHERE id = {id}"
        # todo: return Client.py model client
        querry_result = self.db.execute_read_query(querry)[0]
        print(querry_result)
        query_account = self.account_service.get_accounts_by_client_id(id)
        client = Client(querry_result["id"], querry_result["name"], querry_result["surname"], querry_result["pesel"], query_account,
                        querry_result["login"], None)
        return client
    
    def get_client_by_login(self, login):
        querry_for_id = f"SELECT * FROM clients WHERE login = '{login}'"
        client_id = self.db.execute_read_query(querry_for_id)[0]["id"]
        return self.get_client(client_id)

    def add_client(self, client: Client):
        login = self.create_login(client)
        client.set_login(login)
        self.db.insert_record("clients", client.to_db())

    def create_login(self, client: Client):
        return f"{client.name[0:2]}{client.surname[0:2]}{random.randint(100, 999)}"

    def delete_client(self, client_id):
        query = f"DELETE FROM clients WHERE id = '{client_id}'"
        self.db.execute_query(query)

    def check_password(self, client_login, client_password):
        query = f"SELECT * FROM clients WHERE login = '{client_login}'"
        query_result = self.db.execute_read_query(query)[0]
        password_result = query_result["password"]
        if password_result == client_password:
            return True
        else:
            return False