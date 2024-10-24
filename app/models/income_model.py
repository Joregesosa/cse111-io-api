from models import Model

class Incomes(Model):
    def __init__(self):
        super().__init__()
        self._table = "ingresos"
        
