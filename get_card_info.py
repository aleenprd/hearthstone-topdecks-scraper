"""Scrape HearthstoneTopDecks website for card URLs."""


# IMPORTING PACKAGES
# -------------------------------------- #
import pandas as pd
import pickle
import os
from time import time
from utils import miscelaneous as msc
from utils import scraping as scr


# MAIN METHOD
# -------------------------------------- #
if __name__ == "__main__":
    # Keep track of runtime
    runtime_start = time()
    print("\nCommencing card scraper...")

    # Unpack the configuration options
    # -------------------------------------- #
    config_path = "config/card_scraper_config.json"
    config_options = msc.load_configuration_file(config_path)
    input_path, output_path, failed_output_path, \
        sleep_time = msc.unpack_card_scraper_config(config_options)

    # Unpack list of URLs to parse
    # -------------------------------------- #
    with open(input_path, 'rb') as fp:
        card_url_list = pickle.load(fp)

    # Scrape main page for URL list to parse
    # -------------------------------------- #
    print("\nExtracting card information...")
    card_list, failed_card_list = scr.scrape_multiple_cards(card_url_list, sleep_time)
    df = pd.DataFrame.from_records(card_list)

    # Serialize and save the list for later use
    print("\nSaving cards in CSV...")

    if not os.path.exists("data"):
        os.makedirs("data")

    df.to_csv(output_path, index=False)

    if len(failed_card_list) >= 1:
        with open(failed_output_path, 'wb') as fp:
            pickle.dump(failed_card_list, fp)

    # Keeping track of runtime.
    runtime_end = time()
    print(f"\nFinished in {round(runtime_end-runtime_start,2):,}s...")
