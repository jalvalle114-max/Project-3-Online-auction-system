class User:
    """Represents a user in the auction system."""

    def __init__(self, name: str, balance: float = 100.0):
        """
        Initialize a User.

        Args:
            name (str): The user's name.
            balance (float): Starting balance for the user.
        """
        self.name = name
        self.balance = balance

    def __str__(self):
        return f"{self.name} (${self.balance})"

