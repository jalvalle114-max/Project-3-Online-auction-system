import threading
import time
from datetime import datetime
import random
from colorama import Fore, Style
import platform
import os

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
        self.end_time = datetime.now().timestamp() + duration
        self.last_bid_time = 0 

        self.timer_thread = threading.Thread(target=self._start_timer, daemon=True)
        self.timer_thread.start()

    def _start_timer(self):
        while self.is_open:
            remaining = int(self.end_time - time.time())
            if remaining <= 0:
                with self.lock:
                    self.is_open = False
                    print(f"\n{Fore.YELLOW}Auction '{self.item}' has ended!{Style.RESET_ALL}")
                    self.close()
                break
            time.sleep(1)

    def _beep(self):
        try:
            if platform.system() == "Windows":
                import winsound
                winsound.Beep(1000, 200)
            else:
                os.system("printf '\a'")
        except Exception:
            pass

    def place_bid(self, user, amount):
        with self.lock:
            if not self.is_open:
                print(f"{Fore.RED}Auction '{self.item}' is closed. Cannot place bid.{Style.RESET_ALL}")
                return False

            highest_bid_amount = self.bids[-1].amount if self.bids else self.starting_price

            if amount <= highest_bid_amount:
                print(f"{Fore.RED}Bid too low. Must be higher than ${highest_bid_amount}{Style.RESET_ALL}")
                return False

            if amount > user.balance:
                print(f"{Fore.RED}{user.name} does not have enough balance.{Style.RESET_ALL}")
                return False

            if self.bids:
                self.bids[-1].user.balance += self.bids[-1].amount

            user.balance -= amount
            user.total_bids += 1
            self.bids.append(Bid(user, amount))
            self.last_bid_time = time.time()  
            print(f"{Fore.GREEN}{user.name} placed a bid of ${amount} on {self.item}{Style.RESET_ALL}")
            self._beep()
            return True

    def close(self):
        if not self.bids:
            print(f"{Fore.YELLOW}No bids for {self.item}. No winner.{Style.RESET_ALL}")
            return None
        winner = max(self.bids, key=lambda b: b.amount)
        winner.user.wins += 1
        print(f"{Fore.CYAN}Auction '{self.item}' won by {winner.user.name} with ${winner.amount}{Style.RESET_ALL}")
        self._beep()
        return winner

    def current_highest(self):
        return self.bids[-1].amount if self.bids else self.starting_price

    def time_remaining(self):
        remaining = int(self.end_time - time.time())
        return max(0, remaining)

    def start_bot(self, bots, personalities=None, max_bid_increment=20):

        if personalities is None:
            personalities = {}

        def bot_loop():
            while self.is_open:
                bot = random.choice(bots)
                personality = personalities.get(bot.name, "random")
                increment = random.randint(5, max_bid_increment)
                if personality == "cautious":
                    increment = random.randint(1, 10)
                elif personality == "aggressive":
                    increment = random.randint(10, max_bid_increment)
                if personality == "random" and random.random() < 0.5:
                    time.sleep(random.randint(1, 5))
                    continue

                
                time_since_last_bid = time.time() - self.last_bid_time
                if time_since_last_bid < 2:
                    time.sleep(1)
                    continue

                bid_amount = self.current_highest() + increment
                if bot.balance >= bid_amount:
                    self.place_bid(bot, bid_amount)
                time.sleep(random.randint(2, 5))

        threading.Thread(target=bot_loop, daemon=True).start()


