from service.BaseService import BaseService
from model.Account import Account


class AccountService(BaseService):
    def __init__(self):
        super().__init__()

    def get_accounts_by_client_id(self, client_id):
        query = f"SELECT * FROM accounts WHERE client_id = {client_id}"
        querry_result = self.db.execute_read_query(query)
        account_list = []

        for x in querry_result:
            account = Account(x["account_id"], x["balance"], x["account_type"], x["created_at"], x["client_id"])
            account_list.append(account)
        return account_list

    def add_account(self, account: Account):
        self.db.insert_record("accounts", account.to_db())

    def delete_account(self, client_id):
        query = f"DELETE FROM accounts WHERE client_id = '{client_id}'"
        self.db.execute_query(query)
