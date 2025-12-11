from modules.user import User
from modules.auction import Auction

class AuctionManager:
    def __init__(self):
        self.users = []
        self.auctions = []

    def add_user(self, name, balance=100):
        user = User(name, balance)
        self.users.append(user)
        return user

    def create_auction(self, item, price, duration=30):
        auction = Auction(item, price, duration)
        self.auctions.append(auction)
        return auction

    def list_auctions(self):
        return [str(a) for a in self.auctions]

    def user_leaderboard(self):
        return sorted(self.users, key=lambda u: u.wins, reverse=True)

    def get_user(self, name):
        return next((u for u in self.users if u.name.lower() == name.lower()), None)
