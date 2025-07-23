import decimal

from service.BaseService import BaseService
from model.Account import Account
from model.Transaction import Transaction


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

    def get_account_by_account_id(self, account_id):
        print("Getting account by account id")
        query = f"SELECT * FROM accounts WHERE account_id = '{account_id}'"
        querry_result = self.db.execute_read_query(query)[0]
        print(querry_result)
        account = Account(querry_result["account_id"], querry_result["balance"], querry_result["account_type"],
                          querry_result["created_at"], querry_result["client_id"])
        print("Got account by account id")
        return account

    def math_transaction(self, transaction: Transaction):
        print("calculating balance")
        account = self.get_account_by_account_id(transaction.source_account)
        balance = account.balance
        if transaction.transfer_type == "CREDIT":
            balance -= transaction.value
        else:
            balance += transaction.value
        self.update_account(account.id, balance)
        print("finished calculating balance")

    def update_account(self, id: str, balance: decimal.Decimal):
        print(f"updating account {id} with balance {balance}")
        query = f"""UPDATE accounts SET balance = {balance} WHERE account_id = '{id}'"""
        self.db.execute_query(query)

    def delete_account(self, client_id):
        query = f"DELETE FROM accounts WHERE client_id = '{client_id}'"
        self.db.execute_query(query)
