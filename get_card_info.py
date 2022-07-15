"""Scrape HearthstoneTopDecks website for card URLs."""


# IMPORTING PACKAGES
# -------------------------------------- #
import argparse
import pandas as pd
import pickle
import os
from time import time
from utils import miscelaneous as msc
from utils import scraping as scr


# HELPERS
# -------------------------------------- #
def str2bool(v: str) -> bool:
    """Convert an accepted string representation of a boolean to actual Python boolean values.

    Accepted boolean string representations are lower/uppercase versions of yes/no, true/false and 1/0.
    Args:
        v (str): boolean string representation to be converted.
    Returns:
        A Python boolean.
    """
    v = str(v)
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


# COMMAND LINE ARGUMENTS
# -------------------------------------- #
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config_path",
        type=str,
        default="config/card_scraper_config.json",
        required=False
    )
    parser.add_argument(
        "--download_pics",
        type=str2bool,
        default="False",
        required=False
    )
    return parser.parse_args()


# MAIN METHOD
# -------------------------------------- #
def main(args):
    # Keep track of runtime
    runtime_start = time()
    print("\nCommencing card scraper...")

    # Unpack the configuration options
    # -------------------------------------- #
    config_path = args.config_path

    config_options = msc.load_configuration_file(config_path)
    INPUT_PATH, OUTPUT_PATH, DATAFRAME_FILEPATH, FAILED_DATAFRAME_FILEPATH, \
        IMAGES_PATH, SLEEP_TIME = msc.unpack_card_scraper_config(config_options)

    # Unpack list of URLs to parse
    # -------------------------------------- #
    with open(INPUT_PATH, 'rb') as fp:
        card_url_list = pickle.load(fp)

    # Scrape main page for URL list to parse
    # -------------------------------------- #
    print("\nExtracting card information...")
    card_list, failed_card_list = scr.scrape_multiple_cards(
        card_url_list, args.download_pics, IMAGES_PATH, SLEEP_TIME)
    df = pd.DataFrame.from_records(card_list)

    # Serialize and save the list for later use
    print("\nSaving cards in CSV...")

    if not os.path.exists("data"):
        os.makedirs("data")

    df.to_csv(OUTPUT_PATH + "/" + DATAFRAME_FILEPATH, index=False)

    if len(failed_card_list) >= 1:
        with open(OUTPUT_PATH + "/" + FAILED_DATAFRAME_FILEPATH, 'wb') as fp:
            pickle.dump(failed_card_list, fp)

    # Keeping track of runtime.
    runtime_end = time()
    print(f"\nFinished in {round((runtime_end-runtime_start)/60,2):,}m...")


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
