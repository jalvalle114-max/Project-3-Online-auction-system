from modules.auction_manager import AuctionManager
from tabulate import tabulate
import threading

def display_auctions(manager):
    table = []
    for i, auction in enumerate(manager.auctions, start=1):
        highest_bid = auction.current_highest()
        status = "Open" if auction.is_open else "Closed"
        table.append([i, auction.item, f"${auction.starting_price}", f"${highest_bid}", status])
    print("\n=== Active Auctions ===")
    print(tabulate(table, headers=["ID", "Item", "Starting Price", "Current Highest", "Status"]))

def display_leaderboard(manager):
    table = [[u.name, u.wins, f"${u.balance:.2f}"] for u in manager.user_leaderboard()]
    print("\n=== Leaderboard ===")
    print(tabulate(table, headers=["User", "Wins", "Balance"]))

def display_bid_history(auction):
    table = [[b.user.name, f"${b.amount}", b.time.strftime("%H:%M:%S")] for b in auction.bids]
    print(f"\n--- {auction.item} Bid History ---")
    if table:
        print(tabulate(table, headers=["User", "Amount", "Time"]))
    else:
        print("No bids yet.")

def bid_input_loop(manager):
    while True:
        display_auctions(manager)
        user_name = input("\nEnter your name to bid (or 'exit' to stop): ")
        if user_name.lower() == "exit":
            break
        user = manager.get_user(user_name)
        if not user:
            print("User not found.")
            continue
        try:
            auction_id = int(input("Enter auction ID to bid on: ")) - 1
            auction = manager.auctions[auction_id]
            amount = float(input("Enter your bid amount: "))
            auction.place_bid(user, amount)
        except (ValueError, IndexError):
            print("Invalid input.")

def main():
    manager = AuctionManager()
    print("=== Welcome to the Live Online Auction System ===\n")


    manager.add_user("Alice")
    manager.add_user("Bob")
    manager.add_user("Charlie", balance=200)

 
    manager.create_auction("Vintage Clock", 20, duration=30)
    manager.create_auction("Antique Vase", 50, duration=45)
    manager.create_auction("nightstand" , 55, duration=42)
    manager.create_auction("Rare Artwork", 20, duration=30)
    manager.create_auction("Basketball signed by Lebron", 35, duration=35)

  
    bid_input_loop(manager)

  
    for auction in manager.auctions:
        auction.timer_thread.join()

    print("\n--- Final Auction Results ---")
    for auction in manager.auctions:
        auction.close()
        display_bid_history(auction)

    display_leaderboard(manager)
    print("\nThank you for using the Live Online Auction System!")

if __name__ == "__main__":
    main()
