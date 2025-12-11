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

    def create_auction(self, item, price):
        auction = Auction(item, price)
        self.auctions.append(auction)
        return auction

    def list_auctions(self):
        return [str(a) for a in self.auctions]

    def user_leaderboard(self):
        return sorted(self.users, key=lambda u: u.wins, reverse=True)

    def print_users(self):
        for user in self.users:
            print(f"{user.name} - Balance: ${user.balance:.2f}, Wins: {user.wins}")

    def list_auctions(self):
        return [str(a) for a in self.auctions]
