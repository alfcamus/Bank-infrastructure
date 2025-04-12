from service.BaseService import BaseService


class ClientService(BaseService):
    def __init__(self):
        super().__init__()

    def get_client(self, id):
        query = f"SELECT * FROM clients WHERE id = {id}"
        return super().db.execute_read_query(query)
