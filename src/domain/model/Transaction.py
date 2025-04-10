class Transaction:
    def __init__(self, sourceIban, targetIban, value):
        self.sourceIban = sourceIban
        self.targetIban = targetIban
        self.value = value
        
        