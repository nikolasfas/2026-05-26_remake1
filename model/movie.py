from dataclasses import dataclass


@dataclass
class Movie():
    id: str
    title: str
    income: str

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id