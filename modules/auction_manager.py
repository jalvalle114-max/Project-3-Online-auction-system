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

    def get_user(self, name):
        for user in self.users:
            if user.name == name:
                return user
        return None

    def create_auction(self, item, starting_price, duration=30):
        auction = Auction(item, starting_price, duration)
        self.auctions.append(auction)
        return auction

    def user_leaderboard(self):
        return sorted(self.users, key=lambda u: (-u.wins, -u.balance))

