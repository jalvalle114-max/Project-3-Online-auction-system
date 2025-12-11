class Bid:
    """Represents a bid in an auction."""
    def __init__(self, user, amount):
        self.user = user
        self.amount = amount

class Auction:
    """Represents a single auction."""

    def __init__(self, item: str, starting_price: float):
        """
        Initialize an Auction.

        Args:
            item (str): Item being auctioned.
            starting_price (float): Minimum starting price.
        """
        self.item = item
        self.starting_price = starting_price
        self.bids = []

    def place_bid(self, user, amount):
        """Place a bid on the auction."""
        highest_bid = self.bids[-1].amount if self.bids else self.starting_price
        if amount > highest_bid:
            if user.balance >= amount:
                self.bids.append(Bid(user, amount))
                print(f"Bid accepted: {user.name} bids ${amount}")
            else:
                print(f"{user.name} does not have enough balance for this bid.")
        else:
            print(f"Bid of ${amount} is too low. Current highest bid: ${highest_bid}")

    def close(self):
        """Close the auction and return the winning bid (or None)."""
        if not self.bids:
            return None
        return max(self.bids, key=lambda b: b.amount)

    def __str__(self):
        return f"Auction({self.item}, starting at ${self.starting_price})"

        bid = Bid(user, amount)
        self.bids.append(bid)
        return True

    def highest_bid(self):
        return max(self.bids, default=None)

    def close(self):
        """Close the auction and return winner."""
        self.is_open = False
        return self.highest_bid()
