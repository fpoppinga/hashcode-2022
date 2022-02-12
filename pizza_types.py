from dataclasses import dataclass
from typing import Set


@dataclass
class Client:
    id: int
    likes: Set[str]
    dislikes: Set[str]


@dataclass
class Pizza:
    ingredients: Set[str]

    def to_string(self) -> str:
        return f"{len(self.ingredients)} {' '.join(self.ingredients)}"

