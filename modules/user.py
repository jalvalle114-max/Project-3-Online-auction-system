class User:

    def __init__(self, name: str, balance: float = 100.0):
        self.name = name
        self.balance = balance
        self.total_bids = 0
        self.wins = 0

    def __str__(self):
        return f"{self.name} (${self.balance:.2f})"

