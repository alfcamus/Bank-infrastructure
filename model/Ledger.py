class LedgerEntry:
    def __init__(self, id, iban, transfer_type, value):
        self.id = id
        self.iban = iban
        self.transfer_type = transfer_type
        self.value = value 

class Ledger:
    def __init__(self, ledger_entries):
        self.ledger_entries = ledger_entries