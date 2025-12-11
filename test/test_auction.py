import unittest
from modules.user import User
from modules.auction import Auction

class TestAuction(unittest.TestCase):
    def test_bidding(self):
        alice = User("Alice", 100)
        auction = Auction("Test Item", 10)
        auction.place_bid(alice, 15)
        winner = auction.close()
        self.assertEqual(winner.user.name, "Alice")
        self.assertEqual(winner.amount, 15)

if __name__ == "__main__":
    unittest.main()
