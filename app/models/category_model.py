from models.model import Model

class Category(Model):
    def __init__(self):
        super().__init__()
        self._table = "categories"
        
