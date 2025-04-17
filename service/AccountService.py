from service.BaseService import BaseService
from model.Account import Account

class AccountService(BaseService):
    def __init__(self):
        super().__init__()

    def get_account_by_client_id(self, client_id):
        query = f"SELECT * FROM accounts WHERE client_id = {client_id}"
        # todo: return Client.py model client
        querry_result = self.db.execute_read_query(query)[0]
        account = Account(querry_result["account_id"], querry_result["balance"], querry_result["account_type"], querry_result["created_at"], querry_result["client_id"]) 
        return account

    def add_account(self, account: Account):
        self.db.insert_record("accounts", account.to_db())
    
    def delete_account(self, client_id):
        query = "DELETE FROM accounts WHERE client_id = %s"
        self.db.execute_query(query, (client_id))