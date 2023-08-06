class CharacterNotFoundException(Exception):

    def __init__(self, character: str, *args: object) -> None:
        super().__init__(*args)
        self.character = character

    def __str__(self) -> str:
        return f"Character {self.character} does not exist!"

class NoActiveCharacterException(Exception):
    def __init__(self, player: str, *args: object) -> None:
        super().__init__(*args)
        self.player = player

    def __str__(self) -> str:
        return f"Player {self.player} has no active character!"

class PlayerNotFoundException(Exception):
    def __init__(self, player: str, *args: object) -> None:
        super().__init__(*args)
        self.player = player

    def __str__(self) -> str:
        return f"Player with id {self.player} does not exist!"

class InsufficientFundsException(Exception):

    def __init__(self, character: str, *args: object) -> None:
        super().__init__(*args)
        self.character = character

    def __str__(self) -> str:
        return f"Character {self.character} has not enough money to complete this operation!"

class ItemNotFoundException(Exception):

    def __init__(self, item:str, *args: object) -> None:
        super().__init__(*args)
        self.item = item

    def __str__(self) -> str:
        return f"Item {self.item} does not exist!"

class InsufficientItemsException(Exception):

    def __init__(self, character: str, item: str, *args: object) -> None:
        super().__init__(*args)
        self.character = character
        self.item = item

    def __str__(self) -> str:
        return f"Character {self.character} has not enough {self.item} to complete this operation!"