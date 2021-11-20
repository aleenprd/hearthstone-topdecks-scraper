"""
Scrape HearthstoneTopDecks website for failed cards.

Improvement: Automate this process with If-Else condition.
If the card has characteristics of minion => minion. Etc.
"""


# IMPORTING PACKAGES
# -------------------------------------- #
import pandas as pd
import os
from time import time
from utils import scraping as scr


# MAIN METHOD
# -------------------------------------- #
if __name__ == "__main__":
    # Keep track of runtime
    runtime_start = time()
    print("\nCommencing card scraper...")

    # Manually constructed dict of URLs and card types
    # -------------------------------------- #
    failed_cards_dict = {
        "https://www.hearthstonetopdecks.com/cards/siegebreaker/": ["Minion", 5, 8],
        "https://www.hearthstonetopdecks.com/cards/subject-9/": ["Minion", 4, 4],
        "https://www.hearthstonetopdecks.com/cards/breath-of-the-infinite/": ["Spell", 0, 0]
    }

    # Initialize output
    # -------------------------------------- #
    failed_card_list = []

    # Scrape main page for URL list to parse
    # -------------------------------------- #
    print("\nExtracting failed card information...")
    for url in failed_cards_dict.keys():
        card = scr.scrape_card_manually(
            url,
            card_type=failed_cards_dict[url][0],
            attack=failed_cards_dict[url][1],
            health=failed_cards_dict[url][2])

        failed_card_list.append(card)

    df = pd.DataFrame.from_records(failed_card_list)

    # Serialize and save the list for later use
    print("\nSaving failed cards in CSV...")

    if not os.path.exists("data"):
        os.makedirs("data")

    df.to_csv("data/hstd_failed_cards.csv", index=False)

    # Keeping track of runtime.
    runtime_end = time()
    print(f"\nFinished in {round(runtime_end-runtime_start,2):,}s...")
