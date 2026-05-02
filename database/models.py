from dataclasses import dataclass
@dataclass
class Transaction:
    id : int
    type : str
    amount : float
    category : str
    description : str
    date : str