from modules.auction_manager import AuctionManager

def main():
    manager = AuctionManager()
    print("=== Welcome to the Online Auction System ===\n")


    alice = manager.add_user("Alice")
    bob = manager.add_user("Bob")
    charlie = manager.add_user("Charlie", balance=200)

    clock = manager.create_auction("Vintage Clock", 20)
    vase = manager.create_auction("Antique Vase", 50)

    clock.place_bid(alice, 25)
    clock.place_bid(bob, 30)
    clock.place_bid(charlie, 50)

    vase.place_bid(alice, 60)
    vase.place_bid(charlie, 80)

    print("\n--- Auction Histories ---")
    for auction in manager.auctions:
        print(f"\n{auction.item} Bid History:")
        for line in auction.bid_history():
            print("  " + line)

    print("\n--- Closing Auctions ---")
    for auction in manager.auctions:
        auction.close()

    print("\n--- Leaderboard ---")
    for user in manager.user_leaderboard():
        print(f"{user.name} - Wins: {user.wins}, Balance: ${user.balance:.2f}")

if __name__ == "__main__":
    main()
