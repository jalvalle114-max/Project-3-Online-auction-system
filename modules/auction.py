from datetime import datetime

class Bid:

    def __init__(self, user, amount):
        self.user = user
        self.amount = amount
        self.time = datetime.now()

class Auction:

    def __init__(self, item: str, starting_price: float):
        self.item = item
        self.starting_price = starting_price
        self.bids = []

    def place_bid(self, user, amount):
        highest_bid_amount = self.bids[-1].amount if self.bids else self.starting_price

        if amount <= highest_bid_amount:
            print(f"Bid too low. Must be higher than ${highest_bid_amount}")
            return

        if amount > user.balance:
            print(f"{user.name} does not have enough balance.")
            return

        if self.bids:
            self.bids[-1].user.balance += self.bids[-1].amount

        user.balance -= amount
        user.total_bids += 1
        self.bids.append(Bid(user, amount))
        print(f"{user.name} placed a bid of ${amount} on {self.item}")

    def close(self):
        if not self.bids:
            print(f"No bids for {self.item}. No winner.")
            return None
        winner = max(self.bids, key=lambda b: b.amount)
        winner.user.wins += 1
        print(f"Auction '{self.item}' won by {winner.user.name} with ${winner.amount}")
        return winner

    def bid_history(self):
        return [
            f"{bid.user.name} bid ${bid.amount} at {bid.time.strftime('%H:%M:%S')}"
            for bid in self.bids
        ]

    def current_highest(self):
        return self.bids[-1].amount if self.bids else self.starting_price

    def __str__(self):
        highest = self.current_highest()
        return f"Auction({self.item}, Current Highest: ${highest})"
