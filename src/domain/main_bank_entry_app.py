from model.Account import Account
from model.TransferType import TransferType


# apka powinna wstać - tzn. powinine podnieść się serwerek, który będize obsługiwał połączenia pod localhost:5000, powinna być możliwość dodania klienta przez ClientController oraz sprawdzenie salda przez BalanceController

def make_transaction(source_account: Account, target_account: Account, transfer_type: TransferType, value: float):
    if transfer_type == TransferType.CR:
        source_account.balance -= value
        target_account.balance += value
    else:
        source_account.balance += value
        target_account.balance -= value
        
        
src_acc = Account(1, 1250.00)
trg_acc = Account(2, 2500.00)
print(f"przed source: {src_acc}")
print(f"przed target: {trg_acc}")
tr_type = TransferType.CR
val = 750.00

make_transaction(src_acc, trg_acc, tr_type, val)

print(f"po source: {src_acc}")
print(f"po target: {trg_acc}")