from service.BaseService import BaseService
from model.Transaction import Transaction
from model.TransferType import TransferType  # Assuming you have this enum
import uuid
from datetime import datetime

class TransactionService(BaseService):
    def __init__(self):
        super().__init__()
    
    def get_transactions_by_account(self, account_id, limit=100):
        query = f"""
        SELECT * FROM transactions 
        WHERE source_account = '{account_id}'
        ORDER BY created_at DESC
        LIMIT {limit}
        """
        query_result = self.db.execute_read_query(query)
        transaction_list = []
        
        for x in query_result:
            transaction = Transaction(
                transaction_id=x["transaction_id"],
                source_account=x["source_account"],
                value=x["value"],
                transaction_type=TransferType(x["transfer_type"]),
                created_at=x["created_at"]
            )
            transaction_list.append(transaction)
        return transaction_list
    
    def get_transaction_by_id(self, transaction_id):
        query = f"SELECT * FROM transactions WHERE transaction_id = '{transaction_id}'"
        result = self.db.execute_read_query(query)
        if not result:
            return None
            
        x = result[0]
        return Transaction(
            transaction_id=x["transaction_id"],
            source_account=x["source_account"],
            value=x["value"],
            transaction_type=TransferType(x["transaction_type"]),
            created_at=x["created_at"]
        )
    
    def add_transaction(self, transaction: Transaction):
        self.db.insert_record("transactions", transaction.to_db())
        return transaction
    
    