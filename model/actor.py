from dataclasses import dataclass
from datetime import datetime


@dataclass
class Actor():
    id: str
    name: str
    date_of_birth: datetime
    movieId: str


    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id