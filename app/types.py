from dataclasses import dataclass

@dataclass
class Card:
    """Class to represent cards"""
    Id: int
    Name: str
    ImageURL: str
    Type: str
    Rarity: str
    Set: str
    Classes: list[str]
