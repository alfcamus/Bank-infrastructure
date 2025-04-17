from service.BaseService import BaseService
from model.Client import Client

class ClientService(BaseService):
    def __init__(self):
        super().__init__()
        
    def get_client(self, id):
        query = f"SELECT * FROM clients WHERE id = {id}"
        # todo: return Client.py model client
        querry_result = self.db.execute_read_query(query)[0]
        client = Client(querry_result["id"], querry_result["name"], querry_result["pesel"], None) 
        return client

    def add_client(self, client: Client):
        self.db.insert_record("clients", client.to_db())