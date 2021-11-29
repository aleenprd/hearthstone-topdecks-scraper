"""Miscelaneous functions."""


import json
import os
import sys
from typing import Dict, List
import hashlib


def read_json_local(path: str):
    """Read JSON from local path."""
    with open(path, 'r') as f:
        file = json.load(f)
    return file


def load_configuration_file(optionsPath: str):
    """
    Checks if the file that's searched (specifically options in JSON)
    and reads the file to memory if found and content is correct.
    """
    if os.path.isfile(optionsPath):
        optionsFile = read_json_local(optionsPath)
        if len(optionsFile) == 0:
            print("*\nEmpty options file.")
            return False
        else:
            return optionsFile
    else:
        print("*\nMissing or wrongly named options file.")
        return False


def unpack_url_scraper_config(config_options: Dict) -> List:
    """Unpack url scraper configuration."""
    if config_options is False:
        print("\nMissing, empty or wrongly named config file. \
            Program will terminate.")
        sys.exit()
    else:
        print("\nFetching options from configuration file: ")
        print("# -------------------------------------- #")
        for option in config_options.keys():
            print(f"\t* {option}: {config_options[option]}")
        print()
        main_url = config_options["MAIN_URL"]
        output_path = config_options["OUTPUT_PATH"]
        sleep_time = config_options["SLEEP_TIME"]

    return [main_url, output_path, sleep_time]


def unpack_card_scraper_config(config_options: Dict) -> List:
    """Unpack card scraper configuration."""
    if config_options is False:
        print("\nMissing, empty or wrongly named config file. \
            Program will terminate.")
        sys.exit()
    else:
        print("\nFetching options from configuration file: ")
        print("# -------------------------------------- #")
        for option in config_options.keys():
            print(f"\t* {option}: {config_options[option]}")
        print()
        input_path = config_options["INPUT_PATH"]
        output_path = config_options["OUTPUT_PATH"]
        failed_output_path = config_options["FAILED_OUTPUT_PATH"]
        sleep_time = config_options["SLEEP_TIME"]

    return [input_path, output_path, failed_output_path, sleep_time]


def encode_list(lis: str) -> List:
    """Encode a list of strings."""
    k = map(lambda x: hashlib.md5(x.encode('utf-8')), lis)
    k = [x.hexdigest() for x in k]

    return k


def decode_hash(orig: List, encr: str) -> str:
    """Decode an encrypted string back to original."""
    for i in orig:
        if i == encr:
            return i
        else:
            return None
