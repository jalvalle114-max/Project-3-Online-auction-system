from modules.auction_manager import AuctionManager
from tabulate import tabulate
from colorama import Fore, Style
import time
import threading
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_auctions(manager):
    table = []
    for i, auction in enumerate(manager.auctions, start=1):
        highest_bid = auction.current_highest()
        remaining = auction.time_remaining()
        status = f"{Fore.GREEN}Open{Style.RESET_ALL}" if auction.is_open else f"{Fore.RED}Closed{Style.RESET_ALL}"
        table.append([i, auction.item, f"${auction.starting_price}", f"${highest_bid}", f"{remaining}s", status])
    print(tabulate(table, headers=["ID", "Item", "Starting Price", "Current Highest", "Time Left", "Status"]))

def display_leaderboard(manager):
    table = [[u.name, u.wins, f"${u.balance:.2f}", u.total_bids] for u in manager.user_leaderboard()]
    print("\n=== Leaderboard ===")
    print(tabulate(table, headers=["User", "Wins", "Balance", "Total Bids"]))

def display_bid_history(auction):
    print(f"\n--- {auction.item} Bid History ---")
    if auction.bids:
        for bid in auction.bids:
            print(f"{bid.time.strftime('%H:%M:%S')} - {bid.user.name} bid ${bid.amount}")
    else:
        print("No bids yet.")

def bid_input_loop(manager):
    while True:
        clear_console()
        print(f"{Fore.YELLOW}=== Live Online Auction System ==={Style.RESET_ALL}")
        display_auctions(manager)
        display_leaderboard(manager)
        print("\nType 'exit' to quit, 'history <auction_id>' to see bid history")
        user_name = input("Enter your name to bid: ")
        if user_name.lower() == "exit":
            break
        user = manager.get_user(user_name)
        if not user:
            print(f"{Fore.RED}User not found.{Style.RESET_ALL}")
            time.sleep(1)
            continue
        command = input("Enter 'bid <auction_id> <amount>' or command: ").split()
        if not command:
            continue
        if command[0] == "bid" and len(command) == 3:
            try:
                auction_id = int(command[1]) - 1
                amount = float(command[2])
                auction = manager.auctions[auction_id]
                auction.place_bid(user, amount)
            except Exception as e:
                print(f"{Fore.RED}Invalid input: {e}{Style.RESET_ALL}")
                time.sleep(1)
        elif command[0] == "history" and len(command) == 2:
            try:
                auction_id = int(command[1]) - 1
                auction = manager.auctions[auction_id]
                display_bid_history(auction)
                input("Press Enter to continue...")
            except Exception as e:
                print(f"{Fore.RED}Invalid input: {e}{Style.RESET_ALL}")
                time.sleep(1)

def main():
    manager = AuctionManager()

    manager.add_user("Alice")
    manager.add_user("Bob")
    manager.add_user("Charlie", balance=200)

    bots = [
        manager.add_user("Bot1", balance=500),
        manager.add_user("Bot2", balance=500),
        manager.add_user("Bot3", balance=500)
    ]

    personalities = {
        "Bot1": "aggressive",
        "Bot2": "cautious",
        "Bot3": "random"
    }

    items = [
        ("Vintage Clock", 20, 40),
        ("Antique Vase", 50, 60),
        ("Painting", 100, 50),
        ("Rare Coin", 75, 45),
        ("Jewelry Set", 150, 70)
    ]

    for name, price, duration in items:
        auction = manager.create_auction(name, price, duration)
        auction.start_bot(bots, personalities)

    bid_input_loop(manager)

    for auction in manager.auctions:
        auction.timer_thread.join()

    print(f"\n{Fore.YELLOW}--- Final Auction Results ---{Style.RESET_ALL}")
    for auction in manager.auctions:
        auction.close()
        display_bid_history(auction)

    display_leaderboard(manager)
    print(f"\n{Fore.YELLOW}Thank you for using the Live Online Auction System!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
