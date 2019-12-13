from enum import Enum


class TaxisPolicy(Enum):
    NONE = 1
    MAXPASSAGER=2

class ClientsPolicy(Enum):
    NONE=1
    COHESION = 2
