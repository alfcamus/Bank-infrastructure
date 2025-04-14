from service.BaseService import BaseService


class ClientService(BaseService):
    def __init__(self):
        super().__init__()

    def get_client(self, id):
        query = f"SELECT * FROM clients WHERE id = {id}"
        # todo: return Client.py model client
        return super().db.execute_read_query(query)

    def add_client(self):
        raise NotImplementedError()