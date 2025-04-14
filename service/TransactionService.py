from service.BaseService import BaseService


class TransactionService(BaseService):
    def __init__(self):
        super().__init__()

    def get_transactions(self):
        raise NotImplementedError()
