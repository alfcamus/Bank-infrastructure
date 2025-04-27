class Transaction:
    def __init__(self, source_account, value, transfer_type, transaction_id):
        self.source_account = source_account
        self.value = value
        self.transfer_type = transfer_type
        self.transaction_id = transaction_id
        
    def to_db(self):
        return {'source_account': self.source_account, "value": self.value, "transfer_type": self.transfer_type}
    
    def to_dict(self):
        return {'source_account': self.source_account, "value": self.value, "transfer_type": self.transfer_type, "transaction_id" : self.transaction_id} 