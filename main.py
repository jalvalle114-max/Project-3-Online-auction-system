from modules.auction_manager import AuctionManager

def main():
    manager = AuctionManager()
    print("=== Online Auction System ===\n")

    # Create users
    alice = manager.add_user("Alice")
    bob = manager.add_user("Bob")
    charlie = manager.add_user("Charlie", balance=200)

    # Create auction
    auction = manager.create_auction("Vintage Clock", 20)

    # Place bids
    auction.place_bid(alice, 25)
    auction.place_bid(bob, 30)
    auction.place_bid(charlie, 50)

    # Close auction
    winning_bid = auction.close()
    if winning_bid:
        print(f"\nWinner: {winning_bid.user.name} with bid ${winning_bid.amount}")
    else:
        print("\nNo bids placed. No winner.")

if __name__ == "__main__":
    main()
