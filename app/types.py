from dataclasses import dataclass

@dataclass
class Card:
    """Class to represent cards"""
    Name: str
    ImageURL: str
    Type: str
    Rarity: str
    Set: str
    Class: str
