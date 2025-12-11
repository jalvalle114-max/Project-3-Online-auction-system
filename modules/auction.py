import threading
import time
from datetime import datetime
import random
from colorama import Fore, Style

class Bid:
    def __init__(self, user, amount):
        self.user = user
        self.amount = amount
        self.time = datetime.now()

class Auction:
    def __init__(self, item, starting_price, duration=30):
        self.item = item
        self.starting_price = starting_price
        self.bids = []
        self.is_open = True
        self.duration = duration
        self.lock = threading.Lock()
        self.timer_thread = threading.Thread(target=self._start_timer, daemon=True)
        self.timer_thread.start()

    def _start_timer(self):
        time.sleep(self.duration)
        with self.lock:
            self.is_open = False
            print(f"\n{Fore.YELLOW}Auction '{self.item}' has ended!{Style.RESET_ALL}")
            self.close()

    def place_bid(self, user, amount):
        with self.lock:
            if not self.is_open:
                print(f"{Fore.RED}Auction '{self.item}' is closed. Cannot place bid.{Style.RESET_ALL}")
                return

            highest_bid_amount = self.bids[-1].amount if self.bids else self.starting_price

            if amount <= highest_bid_amount:
                print(f"{Fore.RED}Bid too low. Must be higher than ${highest_bid_amount}{Style.RESET_ALL}")
                return

            if amount > user.balance:
                print(f"{Fore.RED}{user.name} does not have enough balance.{Style.RESET_ALL}")
                return

            if self.bids:
                self.bids[-1].user.balance += self.bids[-1].amount

            user.balance -= amount
            user.total_bids += 1
            self.bids.append(Bid(user, amount))
            print(f"{Fore.GREEN}{user.name} placed a bid of ${amount} on {self.item}{Style.RESET_ALL}")

    def close(self):
        if not self.bids:
            print(f"{Fore.YELLOW}No bids for {self.item}. No winner.{Style.RESET_ALL}")
            return None
        winner = max(self.bids, key=lambda b: b.amount)
        winner.user.wins += 1
        print(f"{Fore.CYAN}Auction '{self.item}' won by {winner.user.name} with ${winner.amount}{Style.RESET_ALL}")
        return winner

    def bid_history(self):
        return [
            f"{bid.user.name} bid ${bid.amount} at {bid.time.strftime('%H:%M:%S')}"
            for bid in self.bids
        ]

    def current_highest(self):
        return self.bids[-1].amount if self.bids else self.starting_price

    def __str__(self):
        highest = self.current_highest()
        status = f"{Fore.GREEN}Open{Style.RESET_ALL}" if self.is_open else f"{Fore.RED}Closed{Style.RESET_ALL}"
        return f"Auction({self.item}, Current Highest: ${highest}, Status: {status})"

    def start_bot(self, bots, max_bid_increment=20, min_interval=3, max_interval=8):
        def bot_loop():
            while self.is_open:
                bot = random.choice(bots)
                bid_amount = self.current_highest() + random.randint(1, max_bid_increment)
                if bot.balance >= bid_amount:
                    self.place_bid(bot, bid_amount)
                time.sleep(random.randint(min_interval, max_interval))

        threading.Thread(target=bot_loop, daemon=True).start()
