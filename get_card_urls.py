"""Scrape HearthstoneTopDecks website for card URLs."""


# IMPORTING PACKAGES
# -------------------------------------- #
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
    print("\nCommencing url scraper...")

    # Unpack the configuration options
    # -------------------------------------- #
    config_path = "config/url_scraper_config.json"
    config_options = msc.load_configuration_file(config_path)
    main_url, output_path, \
        sleep_time = msc.unpack_url_scraper_config(config_options)

    # Scrape main page for URL list to parse
    # -------------------------------------- #
    print("\nExtracting links to cards...")
    url_list = scr.parse_query_and_fetch_links(main_url, sleep_time)

    # Serialize and save the list for later use
    print(f"\nSaving list of {len(url_list)} scraped URLs...")

    if not os.path.exists("data"):
        os.makedirs("data")

    with open(output_path, 'wb') as fp:
        pickle.dump(url_list, fp)

    # Keeping track of runtime.
    runtime_end = time()
    print(f"\nFinished in {round(runtime_end-runtime_start,2):,}s...")
