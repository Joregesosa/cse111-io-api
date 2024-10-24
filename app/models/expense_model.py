from models import Model

class Expense(Model):
    def __init__(self):
        super().__init__()
        self._table = "gastos"
        
