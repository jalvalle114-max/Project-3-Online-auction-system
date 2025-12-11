from modules.user import User
from modules.auction import Auction

class AuctionManager:
    """Manages users and auctions."""

    def __init__(self):
        self.users = []
        self.auctions = []

    def add_user(self, name, balance=100):
        """Add a user to the system."""
        user = User(name, balance)
        self.users.append(user)
        return user

    def create_auction(self, item, price):
        """Create a new auction."""
        auction = Auction(item, price)
        self.auctions.append(auction)
        return auction

    def list_auctions(self):
        """List all auctions."""
        return [str(a) for a in self.auctions]
